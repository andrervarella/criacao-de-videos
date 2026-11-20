# PLAYBOOK — GTA Loucura (@gta6_loucura)

> Manual vivo da página. Vale para Claude, ChatGPT, Codex ou quem for trabalhar no conteúdo.
> **Objetivo:** fazer a @gta6_loucura viralizar no Instagram.
> Atualize este arquivo sempre que aprender algo novo (data + fonte na seção "Aprendizados").

---

## 1. Como o André quer trabalhar

- **Autonomia:** a IA decide e executa (pesquisa, edição, legenda, hashtags, horário). Pergunta só quando precisar de algo dele: dinheiro, login, ou uma escolha de gosto. Quando perguntar, explica o porquê em 1 ou 2 linhas.
- **Respostas** em português do Brasil, curtas e didáticas. Passos manuais um por vez, pensados para celular Android.
- **Franqueza:** nunca dizer que algo foi conferido ou testado se não foi.
- **Ensinar no caminho:** quando uma regra do Instagram mudar o que fazemos (ex.: marcar quem não está no vídeo derruba alcance), explicar e anotar aqui.

## 2. Identidade visual

- **Logo:** plaquinha "GTA 6 LOUCURA" com @gta6_loucura → `logo/plaquinha-gta-loucura.png`
- **Paleta:** roxo escuro `#16061F`, rosa neon `#FF2491`, ciano `#2DE6F0`, branco.
- **Fonte:** Montserrat (Black/ExtraBold itálico nos títulos).
- **Fundo dos Reels:** `fundos/fundo-vice-neon-v1.png` (Vice City neon, gerado no ChatGPT).

## 3. Layout de Reels (v3) — regras fixas

Gerado por `scripts/layout_v3.py` a partir de um JSON de textos (ex.: `scripts/textos-exemplo.json`).

| Elemento | Regra |
|---|---|
| Janela do vídeo | 16:9, centro da tela. **Nada pode ficar em cima dela.** |
| Selo "AO VIVO" | Abaixo da janela, lado **esquerdo** (o direito fica sob os botões do Instagram). |
| Etiqueta rosa | Nome do streamer + contexto (ex.: "JORLAN VIEIRA • LIVE DE GTA 6"). |
| Título (2 linhas) | Linha 1 branca, linha 2 rosa. **Gancho chamativo, muda a cada vídeo.** |
| Legenda curta | 2 linhas: o que acontece + o desfecho. |
| Faixa rosa | Chamada para ação (marca um amigo, salva, comenta). |
| Crédito | Pílula com a fonte (canal/live do criador). |
| Contador | "CORTE DO DIA #00X" (cria série). |
| Áreas proibidas | Topo (~100px), lado direito abaixo do meio (botões), base (~260px, legenda do app). |

Montagem: a moldura com janela transparente vai neste repositório público (link `raw.githubusercontent.com`) e o vidIQ `compose` junta a moldura com o trecho do vídeo (`layout: fit`, áudio original).

## 4. Como escolher um corte

- **Poucos trechos** por vídeo, cada um com **contexto + desfecho** engraçado, irônico ou impactante. A piada tem que fazer sentido sozinha.
- **Duração:** ~30s ideal; até 45–60s se a história pedir.
- **Prioridade:** humor e identificação (ex.: "tá pago" de academia), descobertas absurdas do jogo, reações exageradas. **Sem spoiler de história.**
- **Fonte:** preferir a live/canal **original** do streamer, nunca um canal de cortes com marca d'água de terceiros.
- **Como achar:** vidIQ `video_watch` na live inteira (até 6h) com pedido de "momentos mais engraçados com início/fim/punchline e nota viral"; depois `trim_media` + `compose`.
- **Nunca** apagar ou cobrir a marca/crédito de outro criador.

## 5. Legenda do post e hashtags

Modelo:
```
[EMOJI] GANCHO EM CAIXA ALTA 😂
1–2 frases com o contexto e o nome do criador (@ correto, conferido).
Pergunta ou chamada (marca um amigo / comenta / salva) 👇
🎥 Créditos: live do @criador no YouTube
#gta6 #gtavi #tema1 #tema2 #tema3
```
- **Máximo 5 hashtags**, todas descritivas do vídeo. Hashtag hoje serve para classificar o post, não para gerar alcance.
- Escrever palavras-chave na legenda (ex.: "GTA 6", "academia", "Jason"): o Instagram usa o texto para entender o vídeo.
- **Marcar só quem aparece no vídeo** (o criador). Marcar influencers que não estão no vídeo parece spam e pode reduzir alcance.
- **Conferir o @ antes de marcar** (ex.: o Jorlan é @oficialjorlanvieira; o @jorlanvieira é outra pessoa).

## 6. Publicação

- **Formato:** Reels (também aparece na grade). É o formato que chega a quem não segue a página.
- **Ritmo:** 1 Reel por dia, à noite (~19h de Brasília) até termos dados próprios; depois usar o melhor horário dos insights.
- **Depois de postar:** ativar legendas automáticas (Reel → ⋯ → Gerenciar legendas) e responder comentários na primeira hora.
- **Ferramenta:** vidIQ (`video_upload` → `instagram_publish_reel` ou rascunho agendado). Publicar não gasta crédito.

## 7. ⚠️ Regra de originalidade (MAIS IMPORTANTE)

O Instagram corta da recomendação as contas que mais repostam conteúdo dos outros do que criam conteúdo próprio:
- Contas que em 30 dias postam **principalmente** conteúdo de terceiros viram "agregadoras" e perdem alcance para quem não segue.
- Moldura, borda, marca d'água ou crédito na legenda **não** tornam o vídeo original. Edição **substancial** pode contar.
- A conta volta a ser recomendada quando a **maioria** dos posts dos últimos 30 dias é original.

**Regra da casa:** para cada corte de streamer, publicar pelo menos **2 posts originais**:
- Carrossel de notícias com arte própria
- Gameplay do próprio André ("Projeto Maromba")
- Memes e artes feitos por nós
- Análises e dicas com narração

Conferir de vez em quando: Configurações → **Status da conta** no Instagram.

## 8. Ferramentas

| Ferramenta | Para quê |
|---|---|
| vidIQ (MCP) | Pesquisa de tendências, assistir lives, cortar, montar com moldura, publicar |
| AI Producer (OpusClip) | Baixar vídeo (até 30 min), transcrever, legendar (gratuito por tempo limitado) |
| ChatGPT | Gerar imagens de fundo e artes, com prompt feito pelo Claude |
| Este repositório | Hospedar molduras e logos com link público |
| Higgsfield | Criar cenas com IA (intro, comerciais); **não** corta lives |

## 9. Histórico de posts

| Data | Post | Link |
|---|---|---|
| 20/11/2026 | Coringa — "WASTED" em português | https://www.instagram.com/reel/Df-csajHBCj/ |
| 20/11/2026 | Jorlan — "Tá pago sem treinar" (#003) | https://www.instagram.com/reel/Df-lJ2ACap6/ |
| 21/11/2026 | Jorlan — "Perna fina" (#004) | rascunho para 19h07 |
| 22/11/2026 | Jorlan — "Olympia" (#005) | rascunho para 19h07 |

## 10. Aprendizados (adicione no topo)

- **20/11/2026:** O Instagram limita contas que repostam conteúdo dos outros; borda e crédito não tornam o vídeo original; a conta precisa ter maioria de posts originais em 30 dias. Fontes: creators.instagram.com ("Rewarding original creators", 30/04/2026), Buffer, Metricool, Later.
- **20/11/2026:** Hashtags servem para classificar, não para gerar alcance; usar no máximo 5, descritivas. Legenda com palavras-chave ajuda a descoberta. Fontes: SocialPilot, Skeepers, Keywords Everywhere.
- **20/11/2026:** Reels de até 3 minutos podem ir para o Explorar. Fonte: SocialPilot.
- **20/11/2026:** Repositórios úteis no GitHub para estudar: `social-media-skills/skills` (106 skills de redes sociais para agentes) e `Anil-matcha/AI-Youtube-Shorts-Generator` (cortes automáticos com Whisper, roda em PC).
