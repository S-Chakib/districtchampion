const allCards = JSON.parse(document.getElementById('cards-data').textContent);
const container = document.getElementById('imageWrapper');

const grouped = {
  'A-defend': [], 'A-middle': [], 'A-attack': [],
  'B-defend': [], 'B-middle': [], 'B-attack': []
};

const layout = [
  'A-defend', 'A-middle', 'A-attack',
  'B-attack', 'B-middle', 'B-defend'
];

const positionMap = {
  'A-defend': '15%',
  'A-middle': '28%',
  'A-attack': '43%',
  'B-attack': '57%',
  'B-middle': '72%',
  'B-defend': '85%',
};

let remainingCards = [...allCards];

// Initialize weather buttons (team buttons on left/right)
function setupTeamButtons() {
  document.querySelectorAll('.team-button-img').forEach(button => {
    button.addEventListener('click', () => {
      const team = button.dataset.team;
      const index = button.dataset.index;
      alert(`You clicked button ${index} from Team ${team}`);
    });
  });
}

// Build the game layout from grouped data
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
        const imagePath = player.pic ? player.pic.replace(/^\/\/+/, '') : 'pics/standard.jpg';
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

// Handle card selection (chooseCardBtn click)
function setupChooseCardFlow() {
  const chooseBtn = document.getElementById('chooseCardBtn');

  function showCardSelectionModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = "<h5>Select your card:</h5><hr>";

    const myCards = remainingCards.filter(card => {
      const index = allCards.indexOf(card);
      return index < 7; // Team A
    });

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
        <strong>${card.name}</strong> – ${card.role}, ${card.points} points
      `;

      cardDiv.onclick = () => {
        const key = `A-${card.role.toLowerCase()}`;
        grouped[key].push({ ...card, team: 'A' });

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
  const teamBCards = remainingCards.filter(card => {
    const index = allCards.indexOf(card);
    return index >= 7; // Team B
  });

  if (teamBCards.length === 0) {
    console.log("No cards left for Team B");
    return;
  }

  const chosen = teamBCards[Math.floor(Math.random() * teamBCards.length)];
  const key = `B-${chosen.role.toLowerCase()}`;
  grouped[key].push({ ...chosen, team: 'B' });

  remainingCards = remainingCards.filter(c => c !== chosen);

  renderGameLayout();

  // Re-enable player button if more cards remain
  const chooseBtn = document.getElementById('chooseCardBtn');
  const remainingMyCards = remainingCards.filter(card => allCards.indexOf(card) < 7);
  if (remainingMyCards.length > 0) {
    chooseBtn.disabled = false;
  }
}

// Entry point
function initGame() {
  setupTeamButtons();
  setupChooseCardFlow();
  renderGameLayout();
}

document.addEventListener('DOMContentLoaded', initGame);
