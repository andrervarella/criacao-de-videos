# PLAYBOOK — André Varela (@treinadorandrevarela)

> Manual de conteúdo da marca pessoal. Vale para Claude, ChatGPT e Codex.
> **Base:** o que funcionou na GTA Loucura (`../gta-loucura/PLAYBOOK.md`), adaptado para **autoridade em treino**: menos humor, mais conteúdo técnico que as pessoas salvam e compartilham.
> O repositório privado `AV-LANDPAGE-VIDEOS` continua sendo a fonte oficial da marca (identidade, landing page). Aqui fica só o que precisa de link público ou é reaproveitável.

---

## 1. Posicionamento

- **Quem fala:** profissional de educação física, mais de 15 anos de experiência, consultoria esportiva online e personal presencial, preparação de atletas de fisiculturismo.
- **Tom:** autoridade e clareza. Explica o porquê e corta mito. Usa frases da marca, como "O básico executado com excelência torna o resultado inevitável".
- **Objetivo dos posts:** salvamento e compartilhamento (prova de valor), depois DM e agendamento de consulta.

## 2. O que reaproveitamos da GTA Loucura

| Mecanismo | Na GTA Loucura | No André Varela |
|---|---|---|
| Gerador de carrossel | `carrossel_v1.py` + `slides.json` | O mesmo script, com o tema `andre-varela/tema-av.json` (preto, vermelho, prata) |
| Moldura de Reels | `layout_v3.py` (janela 16:9) | Versão AV: vídeo vertical do André falando + título-gancho + legenda queimada (a fazer) |
| Pesquisa de pauta | vidIQ trending e outliers de "GTA 6" | Os mesmos tools com temas de treino, hipertrofia, emagrecimento e mitos de academia |
| Cortes de vídeo longo | vidIQ `video_watch` + `trim_media` | Lives, podcasts e aulas do próprio André → cortes de 30–60s com a melhor explicação |
| Legenda queimada | Instagram automático | AI Producer (OpusClip): transcreve e põe legenda no vídeo do André (grátis por tempo limitado) |
| Publicação | vidIQ (rascunho → agendar) | vidIQ, depois de conectar a conta @treinadorandrevarela no vidIQ |
| Conferência | Baixar o vídeo e ver 4 quadros | Igual. E conferir cada afirmação técnica contra a fonte |
| Repositório público | `criacao-de-videos` | Pasta `andre-varela/` (logo, tema, exemplos) |

## 3. Formatos que mais servem para autoridade

1. **Carrossel educativo (o principal).** Mito × verdade, "3 erros que…", passo a passo de técnica, comparações (ex.: halter × barra).
   - Capa com promessa clara, um ponto por slide, último slide com resumo + "salva" + chamada para consultoria.
2. **Reels do André falando (30–60s).** Gancho nos 2 primeiros segundos ("Você não ganha massa porque…"), legenda queimada, B-roll de treino.
3. **Reels de técnica.** Execução certa × errada, filmada por ele, com setas e textos.
4. **Bastidores e prova social.** Evolução de alunos, só com **autorização por escrito** e sem promessa de resultado.
5. **Cortes de lives e aulas.** Melhores explicações de vídeos longos dele.

**Originalidade:** o conteúdo dele já é original, então a regra de "agregador" da GTA Loucura não preocupa aqui. Mesmo assim, nunca repostar vídeo de outro criador sem edição substancial e crédito.

## 4. Regras de conteúdo técnico (obrigatórias)

- **Toda afirmação técnica precisa de base:** estudo, diretriz ou consenso, citado no rodapé do slide ou na legenda. Na dúvida, escreve "depende" e explica do que depende.
- **Sem promessa de resultado.** Nada de "perca 10 kg em 30 dias" nem antes/depois sem contexto e sem autorização.
- **Nutrição:** falar de princípios gerais (proteína, hidratação, consistência). Plano alimentar e prescrição de dieta são do nutricionista; quando o assunto for esse, indicar o profissional. Suplemento: só com base científica, sem diagnóstico.
- **Segurança:** variações para iniciantes e aviso de procurar avaliação em caso de dor ou lesão.
- Conferir números e comparações antes de postar, no mesmo cuidado da GTA Loucura ("quase o mesmo" ≠ "mais que").

## 5. Identidade visual nos posts

- **Fonte oficial da marca:** o repositório privado `AV-LANDPAGE-VIDEOS` (`AGENTS.md`, `marca/IDENTIDADE_AV.md`, `instagram/PROTOCOLO_EDITORIAL_7_ETAPAS_AV.md`). Em caso de conflito, **o repositório privado vence**.
- **Cores:** preto e grafite (fundo), prata/aço e branco (texto e linhas), vermelho de assinatura `#A11218` usado **só como detalhe**. Estética de luxo discreto, sem brilho exagerado nem clichê de academia.
- **Marca:** "ANDRÉ VARELA" (com um L) + "PERFORMANCE & EVOLUÇÃO". O **monograma AV é intocável**: usar só o arquivo oficial, nunca redesenhar. Em 20/11/2026 o arquivo ainda **não está** em nenhum repositório; quando chegar, vai para `andre-varela/logo/logo-av.png` e o gerador passa a usá-lo no lugar do nome escrito.
- **Fonte:** Montserrat (Black/ExtraBold), títulos em caixa alta.
- **Fotos:** só fotos reais do André, as favoritas ficam em `AV-LANDPAGE-VIDEOS/assets/originais/01_FOTOS_FAVORITAS_USAR_COMO_BASE/`. Elas são privadas: só copiar uma foto para este repositório público (para gerar link) depois que o André aprovar aquele post. Fotos de competição precisam de contexto (não representam a forma atual).
- **Publicação:** no Instagram AV, só posta depois da aprovação do André para cada peça (regra do `AGENTS.md` privado).

## 6. Legenda e hashtags

```
GANCHO (uma linha que dá vontade de ler)
2–4 linhas explicando o ponto principal, com palavras-chave (hipertrofia, treino de perna, emagrecimento…).
Chamada: "Salva pra usar no próximo treino" / "Manda pra quem precisa ouvir isso".
Quer um treino feito para você? Consultoria online: link na bio.
#hipertrofia #treino #musculacao #personaltrainer #consultoriaonline
```
- Máximo 5 hashtags, todas descritivas. Marcar só quem aparece no post.

## 7. Como gerar um carrossel AV

```
cd gta-loucura/scripts
python3 carrossel_v1.py ../../andre-varela/<pasta>/slides.json ../../andre-varela/<pasta>/ ../../andre-varela/tema-av.json
```
O formato do `slides.json` é o mesmo da GTA Loucura (`tipo`, `etiqueta`, `titulo_1/2`, `numero`, `rotulo`, `texto`, `faixa`, `fonte`, `foto_topo`). Exemplo em `andre-varela/exemplos/`.

## 8. Pendências para destravar

- [ ] Enviar o arquivo oficial do monograma AV (o print `Screenshot_20261027_123545_WhatsApp.jpg` ou um PNG/vetor).
- [ ] Conectar @treinadorandrevarela no vidIQ, para postar e agendar.
- [ ] Separar algumas fotos e vídeos de treino do André, para fotos e B-roll.
- [x] Registro no repositório privado: `instagram/MECANISMOS_CRIACAO_CLAUDE_2026-11-20.md`.


## Regra de estilo (20/11/2026)
- **Sem contador de páginas** ("1/7", "2/7") nos carrosséis: o Instagram já mostra e o André acha que deixa cara de feito por IA. Em geral, evitar marcas visuais típicas de template de IA.
- Gerador atual: `andre-varela/scripts/carrossel_av_v1.py` (preto, prata, vermelho #A11218 pontual, logo oficial recortada).

## Histórico de posts
- 20/11/2026 — Carrossel "Caneta emagrecedora sem musculação?" (7 slides, estudo T-REx, Nature Medicine) publicado via Windsor.ai. Media ID 18184665055427475. Arquivos: `andre-varela/posts/2026-11-20-caneta-musculacao-v1/`.

## Aprendizados técnicos (20/11/2026)
- **Publicar no AV: usar o Windsor.ai** (conta `treinadorandrevarela`, ação `create_carousel_post` / `create_video_post`). O plano do vidIQ só aceita 1 Instagram (a GTA Loucura). Se o André trocar a senha, o Windsor pede reconexão.
- **Vídeos do próprio Instagram**: dá para baixar pelo AI Producer (`start_link_download` com o link do Reel) e editar com ffmpeg, sem o André enviar arquivo. Qualidade um pouco menor que o original.
- **Levantamento de Reels**: vidIQ `ig_profile_reels` (5 créditos por 12) + `watch_shortform_content` (10 créditos) para transcrição e trechos.
- Reels com música de terceiros (ex.: capacitação SkyFit com Linkin Park) não servem para reaproveitar o áudio.
- O que mais performa no perfil: o André ensinando/corrigindo de verdade (capacitação 8,9 mil; treino com aluna 3,4 mil e 22 comentários). Conteúdo de IA e de produto fica abaixo.
- Compilado de teste (20/11): `scripts`-livre, feito com ffmpeg — gancho no topo sem cobrir rosto, marca discreta, encerramento com logo. Foi só teste, não postado.
