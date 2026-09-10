const button = document.getElementById("askButton");

const againButton = document.getElementById("againButton");

const questionInput = document.getElementById("question");

const questionScreen = document.getElementById("questionScreen");

const loadingScreen = document.getElementById("loadingScreen");

const resultScreen = document.getElementById("resultScreen");


const loadingMessages = [
    {
        text: "Thinking...",
        emoji: "🤔"
    },
    {
        text: "Consulting the experts...",
        emoji: "🧐"
    },
    {
        text: "Making a very important decision...",
        emoji: "😌"
    },
    {
        text: "Asking the universe...",
        emoji: "✨"
    },
    {
        text: "This requires serious research...",
        emoji: "📚"
    },
    {
        text: "Hmm... interesting...",
        emoji: "👀"
    }
];


button.addEventListener("click", askQuestion);


questionInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});


async function askQuestion() {

    const question = questionInput.value.trim();


    if (question === "") {

        questionInput.placeholder = "You have to ask something 😭";

        return;
    }


    questionScreen.classList.add("hidden");

    resultScreen.classList.add("hidden");

    loadingScreen.classList.remove("hidden");


    const loading =
        loadingMessages[
            Math.floor(Math.random() * loadingMessages.length)
        ];


    document.getElementById("loadingText").innerText =
        loading.text;

    document.getElementById("loadingEmoji").innerText =
        loading.emoji;


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const result = await response.json();


        loadingScreen.classList.add("hidden");

        resultScreen.classList.remove("hidden");


        showResult(result);


    } catch (error) {

        loadingScreen.classList.add("hidden");

        resultScreen.classList.remove("hidden");

        document.getElementById("normalResult")
            .classList.remove("hidden");

        document.getElementById("normalAnswer").innerText =
            "The Oracle is currently asleep. Check that FastAPI and Ollama are running 😭";

    }

}


function showResult(result) {

    document.getElementById("normalResult")
        .classList.add("hidden");

    document.getElementById("yesNoResult")
        .classList.add("hidden");

    document.getElementById("optionsResult")
        .classList.add("hidden");

    againButton.classList.add("hidden");


    if (result.type === "yes_no") {

        showYesNo(result);

    }

    else if (result.type === "options") {

        showOptions(result);

    }

    else {

        showNormal(result);

    }

}


function showYesNo(result) {

    document.getElementById("yesNoResult")
        .classList.remove("hidden");


    document.getElementById("decision").innerText =
        result.decision;


    document.getElementById("yesNoAnswer").innerText =
        result.answer;


    againButton.classList.remove("hidden");

}


function showNormal(result) {

    document.getElementById("normalResult")
        .classList.remove("hidden");


    document.getElementById("normalAnswer").innerText =
        result.answer;


    againButton.classList.remove("hidden");

}


function showOptions(result) {

    document.getElementById("optionsResult")
        .classList.remove("hidden");


    document.getElementById("winnerArea")
        .classList.add("hidden");


    document.getElementById("wheelArea")
        .classList.remove("hidden");


    drawWheel(result.options);


    spinWheel(
        result.options,
        result.winner,
        result.answer
    );

}


const canvas = document.getElementById("wheel");

const ctx = canvas.getContext("2d");


function drawWheel(options, rotation = 0) {

    const center = canvas.width / 2;

    const radius = canvas.width / 2;

    const angle =
        (Math.PI * 2) / options.length;


    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    const colors = [
        "#FFD6E0",
        "#D9F7E8",
        "#FFF0B8",
        "#D9E9FF",
        "#E8D9FF",
        "#FFE2C6"
    ];


    options.forEach((option, index) => {

        const startAngle =
            rotation + index * angle;

        const endAngle =
            startAngle + angle;


        ctx.beginPath();

        ctx.moveTo(center, center);

        ctx.arc(
            center,
            center,
            radius,
            startAngle,
            endAngle
        );

        ctx.closePath();


        ctx.fillStyle =
            colors[index % colors.length];

        ctx.fill();


        ctx.strokeStyle = "#ffffff";

        ctx.lineWidth = 3;

        ctx.stroke();


        ctx.save();


        ctx.translate(center, center);

        ctx.rotate(
            startAngle + angle / 2
        );


        ctx.textAlign = "right";

        ctx.fillStyle = "#333";

        ctx.font = "bold 18px Arial";


        ctx.fillText(
            option,
            radius - 25,
            7
        );


        ctx.restore();

    });

}


function spinWheel(options, winner, comment) {
    const winnerIndex = options.indexOf(winner);

    const slice = (Math.PI * 2) / options.length;

    // The pointer is at the top: -PI / 2
    const pointerAngle = -Math.PI / 2;

    // Center of the winner's slice
    const winnerAngle = winnerIndex * slice + slice / 2;

    // Rotation needed to put winner at the pointer
    const targetRotation = pointerAngle - winnerAngle;

    // Add several full spins
    const extraSpins = 6 * Math.PI * 2;

    const finalRotation = extraSpins + targetRotation;

    const duration = 5000;

    const startTime = performance.now();

    function animate(currentTime) {

        const elapsed = currentTime - startTime;

        const progress = Math.min(elapsed / duration, 1);

        // Smooth slowing down
        const eased = 1 - Math.pow(1 - progress, 4);

        const rotation = finalRotation * eased;

        drawWheel(options, rotation);

        if (progress < 1) {

            requestAnimationFrame(animate);

        } else {

            // Wheel has stopped.
            // Keep it visible for 2 seconds.
            setTimeout(() => {

                showWinner(winner, comment);

            }, 2000);
        }
    }

    requestAnimationFrame(animate);
}


function showWinner(winner, comment) {

    document.getElementById("wheelArea").classList.add("hidden");

    document.getElementById("winnerArea").classList.remove("hidden");

    document.getElementById("winnerOption").innerText = winner;

    document.getElementById("winnerComment").innerText = comment;

    againButton.classList.remove("hidden");
}


againButton.addEventListener("click", function() {

    resultScreen.classList.add("hidden");

    questionScreen.classList.remove("hidden");

    questionInput.value = "";

    questionInput.focus();

});