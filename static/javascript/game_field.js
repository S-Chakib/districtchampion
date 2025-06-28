const groupedCards = JSON.parse(document.getElementById('cards-data').textContent);
const container = document.getElementById('imageWrapper');

const teamAUser = "{{ team_a_user }}";
const teamBUser = "{{ team_b_user }}";

// Flatten grouped cards for convenience (optional)
const teamAPlayers = [...groupedCards.A.players];
const teamBPlayers = [...groupedCards.B.players];
const teamASpecial = [...groupedCards.A.specials];
const teamBSpecial = [...groupedCards.B.specials];
const teamATrainer = [...groupedCards.A.trainer];
const teamBTrainer = [...groupedCards.B.trainer];


let remainingCards = [
  ...teamAPlayers,
  ...teamBPlayers,
  ...teamASpecial,
  ...teamBSpecial
];

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

function setupTeamButtons() {
  document.querySelectorAll('.team-button-img').forEach(button => {
    button.addEventListener('click', () => {
      const team = button.dataset.team;
      const index = button.dataset.index;
      alert(`You clicked button ${index} from Team ${team}`);
    });
  });
}

function renderGameLayout() {
  container.querySelectorAll('.main-card').forEach(el => el.remove());

  let teamACount = 1;
  let teamBCount = 1;

  layout.forEach(key => {
    const mainCard = document.createElement('div');
    mainCard.classList.add('main-card');
    mainCard.style.left = positionMap[key];

    const team = key[0] === 'A' ? 'Team A' : 'Team B';
    const weatherIndex = key[0] === 'A' ? teamACount++ : teamBCount++;

    const header = document.createElement('div');
    header.className = 'card-header';
    if (key[0] === 'B') {
      const weatherBtn = document.createElement('button');
      weatherBtn.className = 'weather-btn';
      weatherBtn.style.backgroundImage = `url('${staticPrefix}pics/play_field/Team_${key[0]}_Weather.png')`;
      weatherBtn.onclick = () => alert(`Clicked Weather ${weatherIndex} ${team}`);
      header.appendChild(weatherBtn);
    } else {
      header.textContent = key.toUpperCase().replace('-', ' - ');
    }

    const body = document.createElement('div');
    body.className = 'card-body';
    if (grouped[key].length === 1) body.classList.add('center-single');

    grouped[key].forEach(player => {
      const mini = document.createElement('div');
      mini.className = 'player-mini-card';

      const nameDiv = document.createElement('div');
      nameDiv.className = 'name';
      nameDiv.textContent = player.name;

      const pointsDiv = document.createElement('div');
      pointsDiv.className = 'points';
      pointsDiv.textContent = `Points: ${player.points}`;

      mini.appendChild(nameDiv);
      mini.appendChild(pointsDiv);

      mini.onclick = () => {
        const imagePath = player.pic ? player.pic.replace(/^\/\/+/, '') : 'pics/standard.png';
        document.getElementById('modalBody').innerHTML = `
          <img src='${staticPrefix}${imagePath}' alt='Player Image' class='img-fluid rounded mb-3' style='height: 30vh; width: auto;'>
          <strong>Name:</strong> ${player.name}<br>
          <strong>Team:</strong> ${player.team}<br>
          <strong>Role:</strong> ${player.role}<br>
          <strong>Type:</strong> ${player.type}<br>
          <strong>Points:</strong> ${player.points}`;
        const modal = new bootstrap.Modal(document.getElementById('playerModal'));
        modal.show();
      };

      body.appendChild(mini);
    });

    const footer = document.createElement('div');
    footer.className = 'card-footer';
    if (key[0] === 'A') {
      const weatherBtn = document.createElement('button');
      weatherBtn.className = 'weather-btn';
      weatherBtn.style.backgroundImage = `url('${staticPrefix}pics/play_field/Team_${key[0]}_Weather.png')`;
      weatherBtn.onclick = () => alert(`Clicked Weather ${weatherIndex} ${team}`);
      footer.appendChild(weatherBtn);
    } else {
      footer.textContent = `${grouped[key].length} Player${grouped[key].length !== 1 ? 's' : ''}`;
    }

    mainCard.appendChild(header);
    mainCard.appendChild(body);
    mainCard.appendChild(footer);
    container.appendChild(mainCard);
  });
}

function setupChooseCardFlow() {
  const chooseBtn = document.getElementById('chooseCardBtn');

  function showCardSelectionModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = "<h5>Select your card:</h5><hr>";

    const myCards = remainingCards.filter(card =>
      card.team === 'A' && (card.type === 'player' || card.type === 'special')
    );

    if (myCards.length === 0) {
      modalBody.innerHTML = "<p>No more cards to choose from.</p>";
      chooseBtn.disabled = true;
      return;
    }

    myCards.forEach(card => {
      const cardDiv = document.createElement('div');
      cardDiv.classList.add('selectable-card', 'mb-2', 'p-2', 'border', 'rounded');
      cardDiv.style.cursor = 'pointer';
      cardDiv.innerHTML = `
        <strong>${card.name}</strong>
        <br><em>Type:</em> ${card.type}
        <br><em>Role:</em> ${card.role}
        <br><em>Points:</em> ${card.points}
      `;

      cardDiv.onclick = () => {
        // 🃏 Special card: remove only
        if (card.type === 'special') {
          console.log(`🃏 Special card played by USER: ${card.name} (${card.role})`);

          remainingCards = remainingCards.filter(c => c !== card);
          chooseBtn.disabled = true;

          bootstrap.Modal.getInstance(document.getElementById('playerModal')).hide();
          renderGameLayout();

          setTimeout(() => {
            computerPlaysCard();
          }, 500);

          return; // ❌ Do not place special card on the board
        }

        // 🧍 Normal player card
        const key = `A-${card.role.toLowerCase()}`;
        if (grouped[key]) {
          grouped[key].push({ ...card, team: 'A' });
        } else {
          console.warn(`⚠️ Unknown key: ${key}. Role not mapped in layout.`);
        }

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
  }

  chooseBtn.addEventListener('click', () => {
    showCardSelectionModal();
  });
}


function computerPlaysCard() {
  const teamBCardsLeft = remainingCards.filter(card =>
    card.team === 'B' && (card.type === 'player' || card.type === 'special')
  );

  console.log("Team B remaining cards:", teamBCardsLeft);

  if (teamBCardsLeft.length === 0) {
    console.log("Team B is out of cards");
    return;
  }

  const chosen = teamBCardsLeft[Math.floor(Math.random() * teamBCardsLeft.length)];
  console.log("Computer played:", chosen);

  
  if (chosen.type === 'special') {
    console.log(`Sspecial card played by COMPUTER: ${chosen.name} (${chosen.role})`);

    remainingCards = remainingCards.filter(c => c !== chosen);
    renderGameLayout();

    // ✅ Re-enable button for the user
    const chooseBtn = document.getElementById('chooseCardBtn');
    chooseBtn.disabled = false;
    return;
  }

  const key = `B-${chosen.role.toLowerCase()}`;
  if (grouped[key]) {
    grouped[key].push({ ...chosen, team: 'B' });
  } else {
    console.warn(`Unknown layout key: ${key}. Card not placed.`);
    return;
  }

  remainingCards = remainingCards.filter(c => c !== chosen);
  renderGameLayout();

  const chooseBtn = document.getElementById('chooseCardBtn');
  const teamAPlayableLeft = remainingCards.filter(card =>
    card.team === 'A' && (card.type === 'player' || card.type === 'special')
  );
  chooseBtn.disabled = teamAPlayableLeft.length === 0;
}


function initGame() {
  setupTeamButtons();
  setupChooseCardFlow();
  renderGameLayout();
}

document.addEventListener('DOMContentLoaded', initGame);
