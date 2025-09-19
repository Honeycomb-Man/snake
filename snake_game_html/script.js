// Get the canvas and its 2D context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game constants
const GRID_SIZE = 20;
const SNAKE_COLOR = '#6ded8a';
const FOOD_COLOR = '#ff5f85';
const TEXT_COLOR = '#f0f14e';

// Game state
let snake = [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 },
];
let food = { x: 15, y: 15 };
let dx = 1;
let dy = 0;
let score = 0;

// Handle keyboard input
document.addEventListener('keydown', changeDirection);

function changeDirection(event) {
    const LEFT_KEY = 37;
    const RIGHT_KEY = 39;
    const UP_KEY = 38;
    const DOWN_KEY = 40;

    const keyPressed = event.keyCode;
    const goingUp = dy === -1;
    const goingDown = dy === 1;
    const goingRight = dx === 1;
    const goingLeft = dx === -1;

    if (keyPressed === LEFT_KEY && !goingRight) {
        dx = -1;
        dy = 0;
    }
    if (keyPressed === UP_KEY && !goingDown) {
        dx = 0;
        dy = -1;
    }
    if (keyPressed === RIGHT_KEY && !goingLeft) {
        dx = 1;
        dy = 0;
    }
    if (keyPressed === DOWN_KEY && !goingUp) {
        dx = 0;
        dy = 1;
    }
}

// Main game loop
function gameLoop() {
    if (checkCollision()) {
        drawGameOver();
        return;
    }

    setTimeout(function onTick() {
        clearCanvas();
        moveSnake();
        drawSnake();
        drawFood();
        drawScore();
        // Call gameLoop again
        gameLoop();
    }, 100);
}

function clearCanvas() {
    ctx.fillStyle = '#000'; // Black background for the canvas
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function moveSnake() {
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };
    snake.unshift(head);

    const hasEatenFood = snake[0].x === food.x && snake[0].y === food.y;
    if (hasEatenFood) {
        score += 10;
        generateFood();
    } else {
        snake.pop();
    }
}

function generateFood() {
    food.x = Math.floor(Math.random() * (canvas.width / GRID_SIZE));
    food.y = Math.floor(Math.random() * (canvas.height / GRID_SIZE));
}

function drawSnake() {
    ctx.fillStyle = SNAKE_COLOR;
    snake.forEach(segment => {
        ctx.fillRect(segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
    });
}

function drawFood() {
    ctx.fillStyle = FOOD_COLOR;
    ctx.fillRect(food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
}

function drawScore() {
    ctx.fillStyle = TEXT_COLOR;
    ctx.font = '20px "Press Start 2P", sans-serif';
    ctx.fillText('Score: ' + score, 10, 25);
}

function checkCollision() {
    const head = snake[0];
    // Wall collision
    if (head.x < 0 || head.x * GRID_SIZE >= canvas.width || head.y < 0 || head.y * GRID_SIZE >= canvas.height) {
        return true;
    }
    // Self collision
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }
    return false;
}

function drawGameOver() {
    ctx.fillStyle = TEXT_COLOR;
    ctx.font = '50px "Press Start 2P", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2 - 50);

    ctx.font = '20px "Press Start 2P", sans-serif';
    ctx.fillText('Final Score: ' + score, canvas.width / 2, canvas.height / 2);

    ctx.font = '15px "Press Start 2P", sans-serif';
    ctx.fillText('Refresh to play again', canvas.width / 2, canvas.height / 2 + 50);
}

function drawInitialState() {
    clearCanvas();
    drawSnake();
    drawFood();
    drawScore();
}

// Start the game loop
drawInitialState();
gameLoop();
