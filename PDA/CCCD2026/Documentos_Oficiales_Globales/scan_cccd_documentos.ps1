# Escaneo CCCD 2026 - https://cccd.space/documentos - 05:00 y 17:00
# Clave de comparacion: id numerico del chunk remoto (estable). URLs remotas fijas verificadas.
# Si detecta version nueva: escribe ALERTA_*.txt (notificacion por archivo).
# Email desactivado por decision del usuario 2026-09-21: solo archivo, sin envio.
$ErrorActionPreference = 'Stop'
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logFile = Join-Path $baseDir 'seguimiento_diario.log'
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

function Norm($s) {
  $n = $s.Normalize([System.Text.NormalizationForm]::FormD)
  $sb = New-Object System.Text.StringBuilder
  foreach ($c in $n.ToCharArray()) {
    if ([System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($c) -ne [System.Globalization.UnicodeCategory]::NonSpacingMark) { [void]$sb.Append($c) }
  }
  return $sb.ToString()
}

# id remoto | nombre local (clave ASCII) | fecha | version | tamano | etag | URL remota fija
$baselineRaw = @(
  @(1,  'Reglamento General de Competencia CCCD 2026.pdf', '2026-04-02', '1.0.0', 995588, 'e657442eb0e9a351ce28a88be22302dd', 'https://cccd.space/docs/Reglamento%20General%20de%20Competencia%20CCCD%202026.pdf'),
  @(3,  'Motores Permitidos.pdf', '2026-04-02', '1.0.0', 3325111, 'ba334d8fdf554408bc4712507d50b30b', 'https://cccd.space/docs/Motores%20Permitidos.pdf'),
  @(4,  'Diseno Construccion y Pruebas.pdf', '2026-04-02', '1.0.0', 1242574, '305622807c0172d21d4494f3031e1aca', 'https://cccd.space/docs/Dise%C3%B1o%20Construcci%C3%B3n%20y%20Pruebas.pdf'),
  @(5,  'Norma de Seguridad en Coheteria.pdf', '2026-04-02', '1.0.0', 1093234, '3b0baf8a3fd721d1f99df2e968ce0758', 'https://cccd.space/docs/Norma%20de%20Seguridad%20en%20Coheter%C3%ADa.pdf'),
  @(7,  'Procedimientos de Inspeccion y Certificacion.pdf', '2026-04-02', '1.0.0', 1014632, '76d71af113f8f1235367aeb4ecdf09d5', 'https://cccd.space/docs/Procedimientos%20de%20Inspecci%C3%B3n%20y%20Certificaci%C3%B3n.pdf'),
  @(8,  'Cumplimiento y Evaluacion.pdf', '2026-04-02', '1.0.0', 938997, '4df23dbbb074d0794ebc0ce9608eca6d', 'https://cccd.space/docs/Cumplimiento%20y%20Evaluaci%C3%B3n.pdf'),
  @(9,  'Codigo de Conducta y Responsabilidad de las Delegaciones.pdf', '2026-04-02', '1.0.0', 985014, '358909820b8782793ae2832edd9602f3', 'https://cccd.space/docs/C%C3%B3digo%20de%20Conducta%20y%20Responsabilidad%20de%20las%20Delegaciones.pdf'),
  @(10, 'Guia CanSat.pdf', '2026-08-07', '1.0.0', 1336874, 'ff566af226b19452f5313e43331c1935', 'https://cccd.space/docs/Gu%C3%ADa%20CanSat.pdf')
)
$baseline = @()
foreach ($b in $baselineRaw) {
  $baseline += @{ id = [int]$b[0]; key = Norm($b[1]); file = $b[1]; date = $b[2]; version = $b[3]; size = [int64]$b[4]; etag = $b[5]; url = $b[6] }
}

function Write-Log($msg) {
  $line = '[' + $stamp + '] ' + $msg
  Add-Content -Path $logFile -Value $line -Encoding UTF8
}

try {
  Write-Log 'INICIO escaneo https://cccd.space/documentos'
  $html = Invoke-WebRequest -Uri 'https://cccd.space/documentos' -UseBasicParsing -TimeoutSec 60
  $indexMatch = [regex]::Match($html.Content, '/assets/index-[A-Za-z0-9_-]+\.js')
  if (-not $indexMatch.Success) { throw 'No se encontro bundle index-*.js' }
  $indexUrl = 'https://cccd.space' + $indexMatch.Value
  $indexJs = (Invoke-WebRequest -Uri $indexUrl -UseBasicParsing -TimeoutSec 60).Content
  $docMatch = [regex]::Match($indexJs, 'Documentos-[A-Za-z0-9_-]+\.js')
  if (-not $docMatch.Success) { throw 'No se encontro chunk Documentos-*.js' }
  $docUrl = 'https://cccd.space/assets/' + $docMatch.Value
  Write-Log ('Chunk remoto: ' + $docMatch.Value)
  $docJs = (Invoke-WebRequest -Uri $docUrl -UseBasicParsing -TimeoutSec 60).Content

  $pattern = '\{id:(?<id>\d+)[^}]*?date:"(?<date>[^"]+)",version:"(?<version>[^"]+)"'
  $found = [regex]::Matches($docJs, $pattern)
  Write-Log ('Documentos remotos detectados: ' + $found.Count)
  $seenIds = @()
  $changes = @()

  foreach ($m in $found) {
    $rid = [int]$m.Groups['id'].Value
    $seenIds += $rid
    $rdate = $m.Groups['date'].Value
    $rver = $m.Groups['version'].Value
    $ref = $baseline | Where-Object { $_.id -eq $rid }
    if ($null -eq $ref) {
      $changes += ('DOCUMENTO NUEVO id=' + $rid + ' date=' + $rdate + ' version=' + $rver)
      Write-Log ('DOCUMENTO NUEVO id=' + $rid)
      continue
    }
    try {
      $head = Invoke-WebRequest -Uri $ref.url -Method Head -UseBasicParsing -TimeoutSec 60
      $lenRaw = $head.Headers['Content-Length']
      if ($lenRaw -is [array]) { $lenRaw = $lenRaw[0] }
      $len = [int64]$lenRaw
      $etagRaw = $head.Headers['ETag']
      if ($etagRaw -is [array]) { $etagRaw = $etagRaw[0] }
      $etag = "$etagRaw".Trim('"')
    } catch {
      $changes += ('SIN ACCESO HEAD id=' + $rid + ' ' + $ref.file)
      Write-Log ('SIN ACCESO HEAD id=' + $rid)
      continue
    }
    if ($ref.date -ne $rdate -or $ref.version -ne $rver -or $ref.size -ne $len -or $ref.etag -ne $etag) {
      $changes += ('CAMBIO id=' + $rid + ' ' + $ref.file + ' base(' + $ref.date + '/' + $ref.version + '/' + $ref.size + ') -> remoto(' + $rdate + '/' + $rver + '/' + $len + ')')
      Write-Log ('CAMBIO id=' + $rid + ' ' + $ref.file)
    } else {
      Write-Log ('OK sin cambios id=' + $rid + ' ' + $ref.file + ' v' + $rver)
    }
    $localHit = Get-ChildItem -Path $baseDir -Filter '*.pdf' | Where-Object { (Norm($_.Name)) -eq $ref.key }
    if ($null -eq $localHit) {
      Write-Log ('ADVERTENCIA falta copia local id=' + $rid)
    } elseif ($localHit[0].Length -ne $ref.size) {
      Write-Log ('ADVERTENCIA local alterado id=' + $rid)
    }
  }

  foreach ($b in $baseline) {
    if ($seenIds -notcontains $b.id) {
      $changes += ('DOCUMENTO RETIRADO id=' + $b.id + ' ' + $b.file)
      Write-Log ('DOCUMENTO RETIRADO id=' + $b.id)
    }
  }

  if ($changes.Count -gt 0) {
    $alertName = 'ALERTA_CAMBIO_' + (Get-Date -Format 'yyyy-MM-dd_HH-mm') + '.txt'
    $alertPath = Join-Path $baseDir $alertName
    $changes | Out-File -FilePath $alertPath -Encoding UTF8
    Write-Log ('RESULTADO: ' + $changes.Count + ' cambios. Alerta: ' + $alertName)
    exit 2
  } else {
    Write-Log 'RESULTADO: sin cambios. Local sincronizado.'
    exit 0
  }
} catch {
  Write-Log ('ERROR: ' + $_.Exception.Message)
  exit 1
}
