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

function fetchAndUpdateCards() {
  fetch(`/game/${matchId}/cards/`)
    .then(response => response.json())
    .then(data => {
      groupedCards = data;

      Object.keys(grouped).forEach(key => grouped[key] = []);
      groupedCards.A.forEach(card => {
        if (card.played) {
          const k = `A-${card.p1.toLowerCase()}`;
          if (grouped[k]) grouped[k].push(card);
        }
      });
      groupedCards.B.forEach(card => {
        if (card.played) {
          const k = `B-${card.p1.toLowerCase()}`;
          if (grouped[k]) grouped[k].push(card);
        }
      });

      const teamA = groupedCards.A.filter(c => ['player', 'special'].includes(c.type) && !c.played);
      const teamB = groupedCards.B.filter(c => ['player', 'special'].includes(c.type) && !c.played);
      remainingCards = [...teamA, ...teamB];

      renderGameLayout();
      chooseBtn.disabled = !remainingCards.some(c => c.team === 'A' && (c.type === 'player' || c.type === 'special'));
    })
    .catch(error => console.error("❌ Failed to fetch game cards:", error));
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAndUpdateCards();
  initGame();
});

function initGame() {
  setupTeamButtons();
  setupChooseCardFlow();
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

    const myCards = remainingCards.filter(
      card => card.team === 'A' && !card.played && ['player', 'special'].includes(card.type)
    );
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
        sendCardPlayed(card, 'A');
        chooseBtn.disabled = true;
        bootstrap.Modal.getInstance(document.getElementById('playerModal')).hide();
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
    const cardList = grouped[key] || [];
    const mainCard = document.createElement('div');
    mainCard.className = 'main-card';
    mainCard.style.left = positionMap[key];

    const team = key.startsWith('A') ? 'A' : 'B';

    const header = document.createElement('div');
    header.className = 'card-header p-0';

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
    footer.className = 'card-footer p-0';

    const weatherBtn = document.createElement('button');
    weatherBtn.className = 'weather-btn';
    weatherBtn.style.backgroundImage = `url('${staticPrefix}pics/play_field/Team_${team}_Weather.png')`;
    weatherBtn.onclick = () => {
      alert(`🌦️ Team ${team} clicked on ${key.toUpperCase()}`);
    };

    if (team === 'A') {
      footer.appendChild(weatherBtn);
      mainCard.appendChild(header);
    } else {
      header.appendChild(weatherBtn);
      mainCard.appendChild(header);
    }

    mainCard.appendChild(body);

    if (team === 'A') {
      mainCard.appendChild(footer);
    } else {
      mainCard.appendChild(footer);
    }

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
  sendCardPlayed(card, 'B');
  console.log("🔍 Team B remaining cards:", teamBCardsLeft);
}

function sendCardPlayed(card, team) {
  socket.send(JSON.stringify({
    game_id: matchId,
    card_id: card.id,
    message: `${card.name} played by Team ${team}`,
    card: card,
    team: team,
  }));
  fetchAndUpdateCards();
}

const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsUrl = `${protocol}://${window.location.host}/ws/game/${matchId}/`;
const socket = new WebSocket(wsUrl);

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log("🔁 Message received:", data);

  if (
    (data.card && data.team) ||
    data.effect === "add_points" ||
    data.action === "remove_points" ||
    data.action === "update_from_backend"
  ) {
    fetchAndUpdateCards();
  }
};

socket.onopen = () => console.log("✅ WebSocket open");
socket.onclose = () => console.warn("❌ WebSocket closed");

