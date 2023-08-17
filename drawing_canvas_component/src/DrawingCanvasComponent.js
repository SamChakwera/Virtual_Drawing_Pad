import React, { useState, useRef, useEffect } from 'react';

function DrawingCanvasComponent(props) {
    const canvasRef = useRef(null);
    const [drawing, setDrawing] = useState(false);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        canvas.addEventListener('mousedown', () => setDrawing(true));
        canvas.addEventListener('mouseup', () => {
            setDrawing(false);
            ctx.beginPath();
        });
        canvas.addEventListener('mousemove', draw);

        function draw(event) {
            if (!drawing) return;
            ctx.lineWidth = 10;
            ctx.lineCap = 'round';
            ctx.strokeStyle = 'black';

            ctx.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
        }
    }, []);

    return (
        <div>
            <canvas ref={canvasRef} width="280" height="280" style={{border: '1px solid'}}></canvas>
            <button onClick={() => {
                const dataURL = canvasRef.current.toDataURL();
                props.streamlit.setComponentValue(dataURL);
            }}>
                Capture Drawing
            </button>
        </div>
    );
}

export default DrawingCanvasComponent;
