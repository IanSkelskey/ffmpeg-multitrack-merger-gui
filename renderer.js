const { exec } = require('child_process');

document.getElementById('merge-button').addEventListener('click', () => {
    const files = document.getElementById('video-files').files;

    if (files.length === 0) {
        alert('Please select video files.');
        return;
    }

    const outputArea = document.getElementById('output');
    outputArea.textContent = '';

    Array.from(files).forEach((file) => {
        const filePath = file.path;
        const outputFilePath = filePath.replace(/\.[^/.]+$/, '_combined.mkv');

        const command = `ffmpeg -i "${filePath}" -map 0:v:0 -map 0:a:0 -map 0:a:1 -c:v copy -c:a copy "${outputFilePath}"`;

        exec(command, (error, stdout, stderr) => {
            if (error) {
                outputArea.textContent += `Error processing ${file.name}:\n${stderr}\n\n`;
            } else {
                outputArea.textContent += `Processed ${file.name}:\n${stdout}\n\n`;
            }
        });
    });
});
