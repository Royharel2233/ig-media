#!/usr/bin/env python3
"""Gemini 2.5 TTS synth via Generative Language API, service-account auth."""
import argparse, base64, json, sys, requests

p = argparse.ArgumentParser()
p.add_argument('--key')
p.add_argument('--apikey-file')
p.add_argument('--text', required=True, help='text file (UTF-8)')
p.add_argument('--out', required=True, help='output .wav (PCM 24k mono wrapped)')
p.add_argument('--voice', default='Charon')
p.add_argument('--model', default='gemini-2.5-flash-preview-tts')
p.add_argument('--style', default='')
a = p.parse_args()

headers = {'Content-Type': 'application/json'}
qs = ''
if a.apikey_file:
    qs = '?key=' + open(a.apikey_file).read().strip()
else:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    creds = service_account.Credentials.from_service_account_file(
        a.key, scopes=['https://www.googleapis.com/auth/generative-language',
                       'https://www.googleapis.com/auth/cloud-platform'])
    creds.refresh(Request())
    headers['Authorization'] = f'Bearer {creds.token}'
text = open(a.text, encoding='utf-8').read().strip()
if a.style:
    text = f'{a.style}\n{text}'
body = {
    'contents': [{'parts': [{'text': text}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO'],
        'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': a.voice}}},
    },
}
url = f'https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent'
r = requests.post(url + qs, headers=headers, json=body, timeout=120)
if r.status_code != 200:
    print('GEMINI_TTS_ERROR', r.status_code, r.text[:400]); sys.exit(1)
d = r.json()
part = d['candidates'][0]['content']['parts'][0]
pcm = base64.b64decode(part['inlineData']['data'])
mime = part['inlineData'].get('mimeType', '')
rate = 24000
import re
m = re.search(r'rate=(\d+)', mime)
if m: rate = int(m.group(1))
import struct
hdr = struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 36+len(pcm), b'WAVE', b'fmt ', 16, 1, 1, rate, rate*2, 2, 16, b'data', len(pcm))
open(a.out, 'wb').write(hdr + pcm)
print('WROTE', a.out, len(pcm)//2/rate, 's @', rate)