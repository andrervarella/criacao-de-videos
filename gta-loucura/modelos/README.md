# Modelos padrão da GTA Loucura (aprovados em 21/11/2026)

Fundo oficial: `../fundos/fundo-vice-skyline-v1.png` (arte de Vice City). Letras: Inter Display Black (branco) e Black Italic (rosa / faixa rosa inclinada com risco ciano), no estilo dos carrosséis do André. Sem contador de páginas.

| Modelo | Arquivo | Como gerar com conteúdo |
|---|---|---|
| Vídeo (Reels 1080x1920) | `modelo-video-v6-1080x1920.png` (janela transparente) e `modelo-video-v6-previa.jpg` | `scripts/layout_v6_tela_grande.py roteiro.json saida` com `"fundo": "gta-loucura/fundos/fundo-vice-skyline-v1.png"`, `"escurecer": 95`, `"estilo_letras": "carrossel"` |
| Carrossel (4:5, 1080x1350) | `modelo-carrossel-v2-1080x1350.jpg` | `scripts/carrossel_v2_skyline.py slides.json saida` |

## Vídeo
- Janela do vídeo: 9:16, 800 x 1422, posição x=140, y=360. **Nada por cima da janela.**
- Topo: logo, selo AO VIVO, linha ciano e crédito do streamer (à direita).
- Linha 1 (branca): o que está acontecendo. Linha 2: a piada, na faixa rosa (ou, na abertura, texto rosa gigante com `"destaque": true`).
- Abrir com o clímax (~2s), numerar os momentos (#1, #2...), fechar com pergunta/CTA de compartilhamento.
- O vídeo sai sem música: o André escolhe um som em alta no app ao postar.

## Carrossel
- Título branco + segunda linha rosa gigante + faixa rosa com subtítulo + foto com borda ciano e crédito + chamada final + @ no rodapé.
- Fotos com faixa preta (letterbox) são cortadas automaticamente.
