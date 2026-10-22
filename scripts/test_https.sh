#!/usr/bin/env bash
set -u

BASE_URL="${BASE_URL:-https://localhost:8443}"
OUT="evidence/https-test.txt"

mkdir -p evidence

{
    echo "Project 2 - HTTPS Security Test"
    echo "Date (UTC): $(date -u '+%Y-%m-%d %H:%M:%S')"
    echo "Target: $BASE_URL"
    echo

    for path in /login/ /dashboard/ /; do
        echo "=== GET $path ==="
        curl -k -sS -o /dev/null -D - \
            -w $'\nHTTP_STATUS=%{http_code}\n' \
            "$BASE_URL$path" || echo "CURL_ERROR=$?"
        echo
    done

    echo "=== TLS CERTIFICATE ==="
    if [[ "$BASE_URL" =~ ^https://([^/:]+)(:([0-9]+))? ]]; then
        HOST="${BASH_REMATCH[1]}"
        PORT="${BASH_REMATCH[3]:-443}"
        timeout 10 openssl s_client \
            -connect "$HOST:$PORT" -servername "$HOST" \
            </dev/null 2>/dev/null |
            openssl x509 -noout -subject -issuer -dates 2>&1
    else
        echo "Could not parse HTTPS host from BASE_URL"
    fi
} > "$OUT" 2>&1

echo "Test finished. Results saved to $OUT"
cat "$OUT"
