<!-- components/audio/AudioVisualizer.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';

const props = defineProps({
  isRecording: Boolean,
  audioStream: MediaStream,
  visualizationType: {
    type: String,
    default: 'bars', // 'bars' | 'wave' | 'circle' | 'flower'
  },
  primaryColor: {
    type: String,
    default: '#60A5FA' // Blue
  },
  secondaryColor: {
    type: String,
    default: '#3B82F6' // Darker blue
  },
  sensitivity: {
    type: Number,
    default: 1.2
  },
  smoothingTimeConstant: {
    type: Number,
    default: 0.8
  }
});

const canvasRef = ref(null);
const audioContext = ref(null);
const analyser = ref(null);
const animationFrame = ref(null);
const bufferLength = ref(0);
const dataArray = ref(null);
const lastDrawnArray = ref(null);

// Initialize audio context and analyzer with enhanced settings
const initAudioContext = () => {
  if (!props.audioStream) return;
  
  audioContext.value = new (window.AudioContext || window.webkitAudioContext)();
  analyser.value = audioContext.value.createAnalyser();
  
  // Enhanced analyzer settings
  analyser.value.minDecibels = -90;
  analyser.value.maxDecibels = -10;
  analyser.value.smoothingTimeConstant = props.smoothingTimeConstant;
  
  const source = audioContext.value.createMediaStreamSource(props.audioStream);
  source.connect(analyser.value);
  
  analyser.value.fftSize = 512; // Increased for better resolution
  bufferLength.value = analyser.value.frequencyBinCount;
  dataArray.value = new Uint8Array(bufferLength.value);
  lastDrawnArray.value = new Uint8Array(bufferLength.value);
};

// Smoothing function for transitions
const smoothData = () => {
  if (!lastDrawnArray.value) {
    lastDrawnArray.value = new Uint8Array(dataArray.value);
    return dataArray.value;
  }

  const smoothedArray = new Uint8Array(bufferLength.value);
  for (let i = 0; i < bufferLength.value; i++) {
    smoothedArray[i] = lastDrawnArray.value[i] + 
      (dataArray.value[i] - lastDrawnArray.value[i]) * 0.3;
  }
  
  lastDrawnArray.value = smoothedArray;
  return smoothedArray;
};

// Enhanced bar visualization with gradients and glow
const drawBars = (ctx, canvas) => {
  const smoothedData = smoothData();
  const barWidth = (canvas.width / bufferLength.value) * 2.5;
  let x = 0;
  
  // Add glow effect
  ctx.shadowBlur = 15;
  ctx.shadowColor = props.primaryColor;
  
  for (let i = 0; i < bufferLength.value; i++) {
    const barHeight = (smoothedData[i] / 255) * canvas.height * props.sensitivity;
    
    // Enhanced gradient
    const gradient = ctx.createLinearGradient(
      0, canvas.height - barHeight, 
      0, canvas.height
    );
    gradient.addColorStop(0, props.primaryColor + '80'); // Semi-transparent
    gradient.addColorStop(0.5, props.primaryColor);
    gradient.addColorStop(1, props.secondaryColor);
    
    ctx.fillStyle = gradient;
    
    // Rounded corners for bars
    const radius = Math.min(barWidth / 2, barHeight / 2, 4);
    ctx.beginPath();
    ctx.moveTo(x + radius, canvas.height - barHeight);
    ctx.lineTo(x + barWidth - radius, canvas.height - barHeight);
    ctx.quadraticCurveTo(x + barWidth, canvas.height - barHeight, x + barWidth, canvas.height - barHeight + radius);
    ctx.lineTo(x + barWidth, canvas.height);
    ctx.lineTo(x, canvas.height);
    ctx.lineTo(x, canvas.height - barHeight + radius);
    ctx.quadraticCurveTo(x, canvas.height - barHeight, x + radius, canvas.height - barHeight);
    ctx.closePath();
    ctx.fill();
    
    x += barWidth + 1;
  }
};

// Enhanced wave visualization with smooth curves
const drawWave = (ctx, canvas) => {
  const smoothedData = smoothData();
  ctx.lineWidth = 3;
  ctx.strokeStyle = props.primaryColor;
  ctx.fillStyle = props.primaryColor + '20'; // Light fill
  
  // Create smooth curve
  ctx.beginPath();
  ctx.moveTo(0, canvas.height / 2);
  
  const points = [];
  const sliceWidth = canvas.width / bufferLength.value;
  
  for (let i = 0; i < bufferLength.value; i++) {
    const v = smoothedData[i] / 128.0;
    const y = (v * canvas.height) / 2;
    points.push({ x: i * sliceWidth, y });
  }
  
  // Bezier curve through points
  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  
  for (let i = 1; i < points.length - 2; i++) {
    const xc = (points[i].x + points[i + 1].x) / 2;
    const yc = (points[i].y + points[i + 1].y) / 2;
    ctx.quadraticCurveTo(points[i].x, points[i].y, xc, yc);
  }
  
  ctx.lineTo(canvas.width, canvas.height / 2);
  ctx.lineTo(canvas.width, canvas.height);
  ctx.lineTo(0, canvas.height);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
};

// Enhanced circular visualization with dynamic particles
const drawCircle = (ctx, canvas) => {
  const smoothedData = smoothData();
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const baseRadius = Math.min(centerX, centerY) * 0.8;
  
  // Draw base circle with gradient
  const gradient = ctx.createRadialGradient(
    centerX, centerY, baseRadius * 0.5,
    centerX, centerY, baseRadius
  );
  gradient.addColorStop(0, props.primaryColor + '20');
  gradient.addColorStop(1, props.primaryColor + '05');
  
  ctx.beginPath();
  ctx.arc(centerX, centerY, baseRadius, 0, 2 * Math.PI);
  ctx.fillStyle = gradient;
  ctx.fill();
  
  // Draw dynamic particles
  for (let i = 0; i < bufferLength.value; i++) {
    const amplitude = smoothedData[i] / 255 * props.sensitivity;
    const angle = (i / bufferLength.value) * 2 * Math.PI;
    const radius = baseRadius * (1 + amplitude * 0.3);
    
    const x = centerX + Math.cos(angle) * radius;
    const y = centerY + Math.sin(angle) * radius;
    
    // Particle glow
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, 2 * Math.PI);
    ctx.fillStyle = props.secondaryColor;
    ctx.shadowBlur = 10;
    ctx.shadowColor = props.secondaryColor;
    ctx.fill();
    
    // Connect particles with faded lines
    if (i > 0) {
      const prevAngle = ((i - 1) / bufferLength.value) * 2 * Math.PI;
      const prevRadius = baseRadius * (1 + (smoothedData[i - 1] / 255) * 0.3);
      const prevX = centerX + Math.cos(prevAngle) * prevRadius;
      const prevY = centerY + Math.sin(prevAngle) * prevRadius;
      
      ctx.beginPath();
      ctx.moveTo(prevX, prevY);
      ctx.lineTo(x, y);
      ctx.strokeStyle = props.primaryColor + '40';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }
};

// New flower visualization
const drawFlower = (ctx, canvas) => {
  const smoothedData = smoothData();
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const baseRadius = Math.min(centerX, centerY) * 0.6;
  
  ctx.save();
  ctx.translate(centerX, centerY);
  
  // Draw petals
  for (let i = 0; i < bufferLength.value; i += 2) {
    const amplitude = smoothedData[i] / 255 * props.sensitivity;
    const angle = (i / bufferLength.value) * 2 * Math.PI;
    const petalLength = baseRadius * (0.5 + amplitude * 0.5);
    
    ctx.rotate(angle);
    
    // Create petal gradient
    const gradient = ctx.createLinearGradient(0, 0, petalLength, 0);
    gradient.addColorStop(0, props.primaryColor + '90');
    gradient.addColorStop(1, props.secondaryColor + '40');
    
    // Draw petal
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.quadraticCurveTo(
      petalLength * 0.5, petalLength * 0.2,
      petalLength, 0
    );
    ctx.quadraticCurveTo(
      petalLength * 0.5, -petalLength * 0.2,
      0, 0
    );
    
    ctx.fillStyle = gradient;
    ctx.shadowBlur = 10;
    ctx.shadowColor = props.primaryColor;
    ctx.fill();
    
    ctx.rotate(-angle);
  }
  
  ctx.restore();
};

// Main animation loop with smooth transitions
const animate = () => {
  if (!props.isRecording || !canvasRef.value) return;
  
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  
  analyser.value.getByteFrequencyData(dataArray.value);
  
  // Clear canvas with fade effect
  ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Draw visualization based on selected type
  switch (props.visualizationType) {
    case 'wave':
      drawWave(ctx, canvas);
      break;
    case 'circle':
      drawCircle(ctx, canvas);
      break;
    case 'flower':
      drawFlower(ctx, canvas);
      break;
    default:
      drawBars(ctx, canvas);
  }
  
  animationFrame.value = requestAnimationFrame(animate);
};

// Handle canvas resize
const handleResize = () => {
  if (canvasRef.value) {
    const canvas = canvasRef.value;
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
  }
};

// Watch for recording state changes
watch(() => props.isRecording, (newVal) => {
  if (newVal && props.audioStream) {
    if (!audioContext.value) {
      initAudioContext();
    }
    animate();
  } else {
    if (animationFrame.value) {
      cancelAnimationFrame(animationFrame.value);
    }
  }
});

// Watch for audio stream changes
watch(() => props.audioStream, (newVal) => {
  if (newVal && !audioContext.value) {
    initAudioContext();
  }
});

// Component lifecycle
onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value);
  }
  if (audioContext.value) {
    audioContext.value.close();
  }
});
</script>

<template>
  <div class="relative w-full h-full">
    <canvas 
      ref="canvasRef"
      class="w-full h-full transition-opacity duration-300 rounded-lg"
      :class="{ 'opacity-0': !isRecording }"
    />
  </div>
</template>

<style scoped>
.relative {
  contain: strict;
}

canvas {
  background: transparent;
}
</style>