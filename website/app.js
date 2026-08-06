// ==========================================
// ONCHAIN MUTINEERS INTERACTIVE SCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
    initGallery();
    initSimulator();
    initDigitalSea();
    initNavigation();
    initAudioToggle();
});

/* ==========================================
   NFT SHOWCASE GALLERY LOGIC (DYNAMIC DIVERSIFIED GALLERY)
   ========================================== */
function initGallery() {
    const wrapper = document.getElementById("dynamic-gallery-wrapper");
    if (!wrapper) return;

    // Define 7 dynamic gallery items from the collection
    const GALLERY_ITEMS = [
        { id: 1, tag: "Synth Red BG", rarity: "rare" },
        { id: 10, tag: "Gold Plate Skin", rarity: "legendary" },
        { id: 42, tag: "Cyber Mohawk", rarity: "rare" },
        { id: 100, tag: "Deep Navy BG", rarity: "common" },
        { id: 200, tag: "Robo Parrot Companion", rarity: "rare" },
        { id: 500, tag: "Space Dome", rarity: "common" },
        { id: 888, tag: "Plague Green Skin", rarity: "rare" }
    ];

    // Clear and build cards dynamically
    wrapper.innerHTML = "";
    GALLERY_ITEMS.forEach((item, index) => {
        const card = document.createElement("div");
        card.className = `gallery-card ${index === 0 ? "active" : ""}`;
        card.innerHTML = `
            <img src="./assets/nft_${item.id}.png" alt="Onchain Mutineer #${item.id}">
            <div class="card-info">
                <h3>Onchain Mutineer #${item.id}</h3>
                <span class="tag tag-${item.rarity}">${item.tag}</span>
            </div>
        `;
        wrapper.appendChild(card);
    });

    const cards = wrapper.querySelectorAll(".gallery-card");
    const prevBtn = document.getElementById("gallery-prev");
    const nextBtn = document.getElementById("gallery-next");
    
    let currentIndex = 0;
    let autoSlideInterval;

    if (cards.length === 0) return;

    function showCard(index) {
        cards.forEach((card, i) => {
            if (i === index) {
                card.classList.add("active");
            } else {
                card.classList.remove("active");
            }
        });
    }

    function nextCard() {
        currentIndex = (currentIndex + 1) % cards.length;
        showCard(currentIndex);
    }

    // Auto-slide setup
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextCard, 5000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    function prevCard() {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length;
        showCard(currentIndex);
    }

    // Controls
    nextBtn.addEventListener("click", () => {
        nextCard();
        resetAutoSlide();
    });

    prevBtn.addEventListener("click", () => {
        prevCard();
        resetAutoSlide();
    });

    // Initialize
    showCard(currentIndex);
    startAutoSlide();
}

/* ==========================================
   SATURDAY MUTINY SIMULATOR LOGIC
   ========================================== */
function initSimulator() {
    const nftsRange = document.getElementById("nfts-range");
    const streakRange = document.getElementById("streak-range");
    const vaultRange = document.getElementById("vault-range");

    const nftsVal = document.getElementById("nfts-val");
    const streakVal = document.getElementById("streak-val");
    const vaultVal = document.getElementById("vault-val");

    const multResult = document.getElementById("mult-result");
    const basePower = document.getElementById("base-power");
    const weightedPower = document.getElementById("weighted-power");
    const estPayout = document.getElementById("est-payout");

    // Standard total voting weight of the rest of the crew (Mocked)
    const MOCK_TOTAL_CREW_WEIGHT = 1250;

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function updateCalculations() {
        const nfts = parseInt(nftsRange.value);
        const streak = parseInt(streakRange.value);
        const vault = parseInt(vaultRange.value);

        // Display current slider values
        nftsVal.textContent = nfts;
        streakVal.textContent = `${streak} week${streak === 1 ? "" : "s"}`;
        vaultVal.textContent = formatNumber(vault);

        // 1. Calculate Streak Multiplier (1.0x base + 10% per week, capped at 2.0x after 10 weeks)
        let multiplier = 1.0;
        if (streak > 0) {
            multiplier += streak * 0.1;
        }
        if (multiplier > 2.0) {
            multiplier = 2.0;
        }

        // Display multiplier
        multResult.textContent = `${multiplier.toFixed(1)}x`;

        // 2. Base Power vs Weighted Power
        const baseVotes = nfts;
        const weightedVotes = nfts * multiplier;

        basePower.textContent = `${baseVotes} vote${baseVotes === 1 ? "" : "s"}`;
        weightedPower.textContent = `${weightedVotes.toFixed(1)} vote${weightedVotes === 1.0 ? "" : "s"}`;

        // 3. Estimated Payout calculation:
        // Pool allocated for plunder is 60% of the vault size.
        const plunderPool = vault * 0.60;
        
        // Payout = (userWeight / (totalCrewWeight + userWeight)) * plunderPool
        const userShare = weightedVotes / (MOCK_TOTAL_CREW_WEIGHT + weightedVotes);
        const payoutAmt = Math.round(userShare * plunderPool);

        estPayout.textContent = `${formatNumber(payoutAmt)} $BOOTY`;
    }

    // Hook events
    nftsRange.addEventListener("input", updateCalculations);
    streakRange.addEventListener("input", updateCalculations);
    vaultRange.addEventListener("input", updateCalculations);

    // Initial calculation run
    updateCalculations();
}

/* ==========================================
   DIGITAL SEA CANVAS ANIMATION LOGIC
   ========================================== */
function initDigitalSea() {
    const canvas = document.getElementById("digital-sea");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    function resize() {
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    let offset = 0;
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "rgba(198, 255, 0, 0.4)"; // Bright neon lime green matches user background
        ctx.strokeStyle = "rgba(198, 255, 0, 0.2)";
        ctx.lineWidth = 1.5;

        // Draw overlapping digital waves matching a digital storm sea
        const waves = [
            { amplitude: 22, frequency: 0.004, speed: 0.015, y: canvas.height * 0.70 },
            { amplitude: 14, frequency: 0.007, speed: 0.025, y: canvas.height * 0.78 },
            { amplitude: 7, frequency: 0.011, speed: 0.035, y: canvas.height * 0.86 }
        ];

        waves.forEach((wave) => {
            ctx.beginPath();
            for (let x = 0; x < canvas.width; x += 15) {
                const y = wave.y + Math.sin(x * wave.frequency + offset * wave.speed) * wave.amplitude;
                // Render nodes as tiny squares representing digital bits
                ctx.fillRect(x - 2, y - 2, 4, 4);
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
        });

        // Falling digital rain representing a storm
        ctx.fillStyle = "rgba(198, 255, 0, 0.12)";
        for (let i = 0; i < 20; i++) {
            const px = (Math.sin(i * 150 + offset * 0.008) * 0.5 + 0.5) * canvas.width;
            const py = ((offset * (1 + (i % 4)) * 0.4) % canvas.height);
            ctx.fillRect(px, py, 1.5, 8 + (i % 8)); // rain lengths
        }

        offset++;
        requestAnimationFrame(animate);
    }
    
    animate();
}

/* ==========================================
   CLEAN URL SMOOTH NAVIGATION LOGIC
   ========================================== */
function initNavigation() {
    // Intercept header, footer, and hero button anchor clicks
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href === "#") return;
            
            const targetId = href.substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: "smooth"
                });
                
                // Update history to clean URL (e.g. /staking instead of #staking)
                history.pushState(null, null, "/" + targetId);
            }
        });
    });

    // Handle initial page load scroll for clean paths (e.g. site.site/staking -> scrolls to #staking)
    const path = window.location.pathname.substring(1);
    if (path) {
        const targetElement = document.getElementById(path);
        if (targetElement) {
            setTimeout(() => {
                targetElement.scrollIntoView({ behavior: "smooth" });
            }, 300);
        }
    }
}

/* ==========================================
   WEB AUDIO API DIGITAL OCEAN SYNTHESIZER
   ========================================== */
let audioCtx = null;
let noiseNode = null;
let filterNode = null;
let gainNode = null;
let lfoNode = null;
let masterGainNode = null;
let isAudioActive = false;

function initOceanAudio() {
    if (audioCtx) return;
    
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContextClass();
    
    // 1. Generate White Noise (2-second buffer)
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
        output[i] = Math.random() * 2 - 1;
    }
    
    noiseNode = audioCtx.createBufferSource();
    noiseNode.buffer = noiseBuffer;
    noiseNode.loop = true;
    
    // 2. Bandpass Filter (gives the water swell texture)
    filterNode = audioCtx.createBiquadFilter();
    filterNode.type = 'bandpass';
    filterNode.Q.value = 1.0;
    filterNode.frequency.value = 450; // base center frequency
    
    // 3. Modulator Gain (LFO volume swings)
    gainNode = audioCtx.createGain();
    gainNode.gain.value = 0.08; // base gain
    
    // 4. Master Gain (for smooth fade-in and fade-out volume control)
    masterGainNode = audioCtx.createGain();
    masterGainNode.gain.value = 0.0; // starts silent
    
    // Connections
    noiseNode.connect(filterNode);
    filterNode.connect(gainNode);
    gainNode.connect(masterGainNode);
    masterGainNode.connect(audioCtx.destination);
    
    // 5. Low Frequency Oscillator (LFO)
    // 0.15Hz frequency = 1 cycle every ~6.6 seconds (natural waves timing)
    lfoNode = audioCtx.createOscillator();
    lfoNode.type = 'sine';
    lfoNode.frequency.value = 0.15;
    
    const lfoGainVol = audioCtx.createGain();
    lfoGainVol.gain.value = 0.06; // volume swings from -0.06 to +0.06
    
    const lfoGainFreq = audioCtx.createGain();
    lfoGainFreq.gain.value = 200; // frequency swings from -200Hz to +200Hz
    
    // Connections to LFO
    lfoNode.connect(lfoGainVol);
    lfoGainVol.connect(gainNode.gain);
    
    lfoNode.connect(lfoGainFreq);
    lfoGainFreq.connect(filterNode.frequency);
    
    // Start playback nodes
    noiseNode.start(0);
    lfoNode.start(0);
}

function initAudioToggle() {
    const toggleBtn = document.getElementById('audio-toggle');
    if (!toggleBtn) return;
    
    const toggleText = toggleBtn.querySelector('.audio-text');
    
    toggleBtn.addEventListener('click', async () => {
        if (!audioCtx) {
            initOceanAudio();
        }
        
        // Resume context if suspended (browser security restriction on autoplay)
        if (audioCtx.state === 'suspended') {
            await audioCtx.resume();
        }
        
        if (isAudioActive) {
            // Fade out sound in 1.0 second
            masterGainNode.gain.linearRampToValueAtTime(0.0, audioCtx.currentTime + 1.0);
            toggleBtn.classList.remove('active');
            if (toggleText) toggleText.textContent = 'AMBIENT OFF';
            isAudioActive = false;
        } else {
            // Fade in sound in 1.5 seconds to 0.35 volume
            masterGainNode.gain.linearRampToValueAtTime(0.35, audioCtx.currentTime + 1.5);
            toggleBtn.classList.add('active');
            if (toggleText) toggleText.textContent = 'AMBIENT ON';
            isAudioActive = true;
        }
    });
}
