const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (req, res) => {
    res.send(`<h1>Maybe try adding "/height-model"</h1>`);
});

app.get('/height-model', (req, res) => {
    const { tap_preference, time } = req.query;

    if (tap_preference && time) {
        exec(`python Web_Application/test.py ${time}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return res.send(`Error: ${stderr}`);
            }

            const result = stdout.trim();
            return res.send(`
                <h1>Height Prediction</h1>
                <p>Tap Preference: ${tap_preference}</p>
                <p>Time: ${time} seconds</p>
                <p>Result from Python script: ${result}</p>
                <a href="/height-model">Try again</a>
            `);
        });
    } else {
        res.send(`
            <h1>Height Prediction Model</h1>
            <form action="/height-model" method="POST">
                <label for="tap_preference">Tap Preference:</label>
                <input type="text" id="tap_preference" name="tap_preference" required><br><br>
                <label for="time">Time (seconds):</label>
                <input type="text" id="time" name="time" required><br><br>
                <button type="submit">Submit</button>
            </form>
        `);
    }
});

app.post('/height-model', (req, res) => {
    const { tap_preference, time } = req.body;

    if (tap_preference === undefined || time === undefined) {
        return res.send(`<h1>Please provide both tap preference and time.</h1>`);
    }

    // Redirect to the GET route with query parameters
    res.redirect(`/height-model?tap_preference=${encodeURIComponent(tap_preference)}&time=${encodeURIComponent(time)}`);
});

app.listen(port, () => {
    console.log(`App listening on port: ${port}`);
});
