fetch('../././data/multiple-data.json')
    .then(response => response.json())
    .then(users => {
        const container = document.getElementById('users-card');

        users.forEach(user => {
            const userCard = document.createElement('div');
            userCard.className = "bg-gray-200 w-fit h-fit px-5 py-3 rounded shadow flex items-center space-x-3 hover:cursor-pointer hover:bg-gray-300 transition-all duration-200";
            userCard.innerHTML = `
                <div class = "bg-gray-100 rounded-full h-[2.5rem] w-[2.5rem] p-3 flex items-center justify-center"><span class="text-xl">${user.name[0]}</span></div>
                <div>
                    <p class = "font-semibold">${user.name}</p>
                    <p class = "text-gray-700">${user.email}</p>
                </div>
            `;

            container.appendChild(userCard);
        });
    })
    .catch(error => {
        console.error('Error loading suer data', error);
    })