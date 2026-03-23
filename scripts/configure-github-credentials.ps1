# Script para configurar credenciais do GitHub no Git Credential Manager
# Execute: .\scripts\configure-github-credentials.ps1

Write-Host "=== Configuracao de Credenciais GitHub ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usuario: LucasCinigalia" -ForegroundColor Gray
Write-Host "Cole seu Personal Access Token e pressione Enter:" -ForegroundColor Yellow
Write-Host "(O token sera armazenado de forma segura pelo Git Credential Manager)" -ForegroundColor Gray
Write-Host ""

$plainToken = Read-Host "Token"

if ([string]::IsNullOrWhiteSpace($plainToken)) {
    Write-Host "Erro: Token nao pode ser vazio." -ForegroundColor Red
    exit 1
}

$credential = @"
protocol=https
host=github.com
username=LucasCinigalia
password=$plainToken
"@

$credential | git credential approve

Write-Host ""
Write-Host "Credenciais configuradas com sucesso!" -ForegroundColor Green
Write-Host "Voce ja pode executar: git push origin main" -ForegroundColor Green
