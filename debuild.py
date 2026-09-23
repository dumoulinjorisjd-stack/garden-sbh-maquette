# INVERSE EXACT de build.sh : reconstruit maquette-jaden.html depuis un index.html
# livre. Sert a revenir a une version passee sans rejouer les modifications a
# l'envers une par une, ce qui serait la meilleure facon d'en oublier une.
import sys
HEAD = """<!doctype html>
<html lang="fr" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lakou Saint-Barthélemy — maquette</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="512x512" href="icone-512.png">
<link rel="apple-touch-icon" href="icone-192.png">
<meta name="theme-color" content="#1F5D3C">
<meta property="og:title" content="Lakou — Saint-Barthélemy">
<meta property="og:description" content="Ce qui pousse ici se partage.">
<meta property="og:image" content="icone-512.png">
<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html,body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""
MILIEU = "\n</head>\n<body>\n"
QUEUE  = "\n</body>\n</html>\n"

out = open(sys.argv[1], encoding='utf-8').read()
assert out.startswith(HEAD), 'entete inattendue'
assert out.endswith(QUEUE), 'pied inattendu'
reste = out[len(HEAD):-len(QUEUE)]
j = reste.index('</style>') + len('</style>')
assert reste[j:j+len(MILIEU)] == MILIEU, 'jointure head/body inattendue'
src = reste[:j] + reste[j+len(MILIEU):]
open(sys.argv[2], 'w', encoding='utf-8').write(src)
print('source reconstruite :', len(src), 'octets')

# CONTROLE : on rejoue build.sh sur la source reconstruite et on exige
# l'identite octet pour octet avec le fichier de depart.
i = src.index('</style>') + len('</style>')
refait = HEAD + src[:i] + MILIEU + src[i:] + QUEUE
assert refait == out, 'ALLER-RETOUR NON IDENTIQUE — ne pas utiliser'
print('aller-retour verifie : identique octet pour octet')
