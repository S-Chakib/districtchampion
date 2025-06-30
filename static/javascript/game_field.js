let groupedCards = { A: [], B: [] };
let remainingCards = [];

const container = document.getElementById('imageWrapper');
const chooseBtn = document.getElementById('chooseCardBtn');
const teamAUser = "{{ team_a_user }}";
const teamBUser = "{{ team_b_user }}";

const grouped = {
  'A-defense': [], 'A-middle': [], 'A-attack': [],
  'B-defense': [], 'B-middle': [], 'B-attack': []
};

const layout = [
  'A-defense', 'A-middle', 'A-attack',
  'B-attack', 'B-middle', 'B-defense'
];

const positionMap = {
  'A-defense': '15%',
  'A-middle': '28%',
  'A-attack': '43%',
  'B-attack': '57%',
  'B-middle': '72%',
  'B-defense': '85%',
};

document.addEventListener('DOMContentLoaded', () => {
  fetch(`/game/${matchId}/cards/`)
    .then(response => response.json())
    .then(data => {
      groupedCards = data;

      const teamA = groupedCards.A.filter(c => ['player', 'special'].includes(c.type));
      const teamB = groupedCards.B.filter(c => ['player', 'special'].includes(c.type));
      remainingCards = [...teamA, ...teamB];

      initGame();
    })
    .catch(error => console.error("❌ Failed to load game cards:", error));
});

function initGame() {
  setupTeamButtons();
  setupChooseCardFlow();
  renderGameLayout();
}

function setupTeamButtons() {
  document.querySelectorAll('.team-button-img').forEach(button => {
    button.addEventListener('click', () => {
      alert(`You clicked button ${button.dataset.index} from Team ${button.dataset.team}`);
    });
  });
}

function setupChooseCardFlow() {
  chooseBtn.addEventListener('click', () => {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = "<h5>Select your card:</h5><hr>";

    const myCards = remainingCards.filter(card => card.team === 'A' && ['player', 'special'].includes(card.type));
    if (myCards.length === 0) {
      modalBody.innerHTML = "<p>No more cards to choose from.</p>";
      chooseBtn.disabled = true;
      return;
    }

    myCards.forEach(card => {
      const cardDiv = document.createElement('div');
      cardDiv.className = 'selectable-card mb-2 p-2 border rounded';
      cardDiv.style.cursor = 'pointer';
      cardDiv.innerHTML = `
        <strong>${card.name}</strong><br>
        <em>Type:</em> ${card.type}<br>
        <em>p1:</em> ${card.p1}<br>
        <em>Points:</em> ${card.points}
      `;

      cardDiv.onclick = () => {
        const key = `A-${card.p1.toLowerCase()}`;
        if (card.type === 'special') {
          console.log(`🃏 Special card played by USER: ${card.name} (${card.p1})`);
        } else if (grouped[key]) {
          grouped[key].push({ ...card, team: 'A' });
        }

        sendCardPlayed(card, 'A');
        remainingCards = remainingCards.filter(c => c !== card);
        chooseBtn.disabled = true;

        bootstrap.Modal.getInstance(document.getElementById('playerModal')).hide();
        renderGameLayout();

        setTimeout(() => {
          computerPlaysCard();
        }, 500);
      };

      modalBody.appendChild(cardDiv);
    });

    const modal = new bootstrap.Modal(document.getElementById('playerModal'));
    modal.show();
  });
}

function renderGameLayout() {
  container.querySelectorAll('.main-card').forEach(el => el.remove());

  layout.forEach(key => {
    const cardList = grouped[key];
    const mainCard = document.createElement('div');
    mainCard.className = 'main-card';
    mainCard.style.left = positionMap[key];

    const header = document.createElement('div');
    header.className = 'card-header';
    header.textContent = key.toUpperCase().replace('-', ' - ');

    const body = document.createElement('div');
    body.className = 'card-body';
    if (cardList.length === 1) body.classList.add('center-single');

    cardList.forEach(player => {
      const mini = document.createElement('div');
      mini.className = 'player-mini-card';

      mini.innerHTML = `
        <div class="name">${player.name}</div>
        <div class="points">Points: ${player.points}</div>
      `;
      mini.onclick = () => {
        const imagePath = player.pic?.replace(/^\/\/+/, '') || 'pics/standard.png';
        document.getElementById('modalBody').innerHTML = `
          <img src='${staticPrefix}${imagePath}' class='img-fluid rounded mb-3' style='height: 30vh;'>
          <strong>Name:</strong> ${player.name}<br>
          <strong>Team:</strong> ${player.team}<br>
          <strong>p1:</strong> ${player.p1}<br>
          <strong>Type:</strong> ${player.type}<br>
          <strong>Points:</strong> ${player.points}
        `;
        new bootstrap.Modal(document.getElementById('playerModal')).show();
      };

      body.appendChild(mini);
    });

    const footer = document.createElement('div');
    footer.className = 'card-footer';
    footer.textContent = `${cardList.length} Player${cardList.length !== 1 ? 's' : ''}`;

    mainCard.appendChild(header);
    mainCard.appendChild(body);
    mainCard.appendChild(footer);
    container.appendChild(mainCard);
  });
}

function computerPlaysCard() {
  const teamBCardsLeft = remainingCards.filter(card =>
    card.team === 'B' && ['player', 'special'].includes(card.type)
  );

  if (!teamBCardsLeft.length) {
    console.log("✅ Game over: Team B out of cards");
    return;
  }

  const card = teamBCardsLeft[Math.floor(Math.random() * teamBCardsLeft.length)];
  const key = `B-${card.p1.toLowerCase()}`;

  if (card.type === 'special') {
    console.log(`💥 Special card played by COMPUTER: ${card.name}`);
  } else if (grouped[key]) {
    grouped[key].push({ ...card, team: 'B' });
  }

  sendCardPlayed(card, 'B');
  remainingCards = remainingCards.filter(c => c !== card);

  renderGameLayout();

  const teamAPlayableLeft = remainingCards.filter(card =>
    card.team === 'A' && ['player', 'special'].includes(card.type)
  );
  chooseBtn.disabled = teamAPlayableLeft.length === 0 ? true : false;
}

function sendCardPlayed(card, team) {
  socket.send(JSON.stringify({
    game_id: matchId,
    message: `${card.name} played by Team ${team}`,
    card: card,
    team: team,
  }));
}

const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsUrl = `${protocol}://${window.location.host}/ws/game/${matchId}/`;
const socket = new WebSocket(wsUrl);

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log("🔁 Message received:", data);

  if (data.card && data.team) {
    const key = `${data.team}-${data.card.p1.toLowerCase()}`;
    if (grouped[key]) {
      grouped[key].push(data.card);
      renderGameLayout();
    }
  }

  if (data.effect === "add_points" && data.target_team) {
    Object.entries(grouped).forEach(([key, cards]) => {
      if (key.startsWith(data.target_team)) {
        cards.forEach(card => card.points += data.points);
      }
    });
    renderGameLayout();
  }

  if (data.action === "remove_points") {
    Object.values(grouped).forEach(cards => {
      cards.forEach(card => card.points = Math.max(0, card.points - data.points));
    });
    renderGameLayout();
  }

  if (data.action === "update_from_backend" && data.grouped) {
    Object.entries(data.grouped).forEach(([key, cards]) => {
      grouped[key] = cards;
    });
    renderGameLayout();
  }
};

socket.onopen = () => console.log("✅ WebSocket open");
socket.onclose = () => console.warn("❌ WebSocket closed");

