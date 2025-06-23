    const cards = JSON.parse(document.getElementById('cards-data').textContent);
    const container = document.getElementById('imageWrapper');

    const grouped = {
      'A-defend': [], 'A-middle': [], 'A-attack': [],
      'B-defend': [], 'B-middle': [], 'B-attack': []
    };

    cards.forEach((card, index) => {
      const team = index < 6 ? 'A' : 'B';
      const key = `${team}-${card.role.toLowerCase()}`;
      grouped[key].push({ ...card, team });
    });

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

    let teamACount = 1;
    let teamBCount = 1;

    layout.forEach((key, i) => {
      const mainCard = document.createElement('div');
      mainCard.classList.add('main-card');
      mainCard.style.left = positionMap[key];

      const team = key[0] === 'A' ? 'Team A' : 'Team B';
      const weatherIndex = key[0] === 'A' ? teamACount++ : teamBCount++;

      const weatherButton = document.createElement('button');
      weatherButton.className = 'weather-btn';
      weatherButton.style.backgroundImage = `url('${staticPrefix}pics/play_field/Team_${key[0]}_Weather.png')`;
      weatherButton.onclick = () => alert(`Clicked Weather ${weatherIndex} ${team}`);

      const header = document.createElement('div');
      header.className = 'card-header';
      if (key[0] === 'B') header.appendChild(weatherButton);
      else header.textContent = key.toUpperCase().replace('-', ' - ');

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
        const footerBtn = document.createElement('button');
        footerBtn.className = 'weather-btn';
        footerBtn.style.backgroundImage = `url('${staticPrefix}pics/play_field/Team_${key[0]}_Weather.png')`;
        footerBtn.onclick = () => alert(`Clicked Weather ${weatherIndex} ${team}`);
        footer.appendChild(footerBtn);
      } else {
        footer.textContent = `${grouped[key].length} Player${grouped[key].length !== 1 ? 's' : ''}`;
      }

      mainCard.appendChild(header);
      mainCard.appendChild(body);
      mainCard.appendChild(footer);
      container.appendChild(mainCard);
    });


    document.querySelectorAll('.team-button-img').forEach(button => {
    button.addEventListener('click', () => {
    const team = button.dataset.team;
    const index = button.dataset.index;

    alert(`You clicked button ${index} from Team ${team}`);
    });
    });