// Silva Loader - Premium Features JavaScript
console.log('✓ Premium Features JS Loaded');

// Global state
let selectedProcess = null;
let selectedDll = null;
let currentGameMode = null;
let allProcesses = [];

// Global click handlers (called from HTML onclick)
function handleMinecraftClick() {
    console.log('✓✓✓ MINECRAFT CLICKED ✓✓✓');
    currentGameMode = 'minecraft';
    document.getElementById('injection-controls').classList.add('hidden');
    document.getElementById('minecraft-inject').classList.remove('hidden');
    setTimeout(() => lucide.createIcons(), 50);
}

function handleFpsClick() {
    console.log('✓✓✓ FPS CLICKED ✓✓✓');
    currentGameMode = 'fps';
    document.getElementById('minecraft-inject').classList.add('hidden');
    document.getElementById('injection-controls').classList.remove('hidden');
    setTimeout(() => showProcessSelector(), 50);
}

// Load Announcements
async function loadAnnouncements() {
    try {
        const response = await fetch('/api/announcements');
        const announcements = await response.json();
        const container = document.getElementById('announcements-container');
        
        if (announcements.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-sm">No announcements at this time.</p>';
            return;
        }

        const iconMap = {
            'rocket': 'rocket',
            'crosshair': 'crosshair',
            'crown': 'crown',
            'shield-alert': 'shield-alert',
            'info': 'info',
            'alert-circle': 'alert-circle'
        };

        const typeStyles = {
            'info': 'border-blue-500/30 bg-blue-500/10',
            'success': 'border-green-500/30 bg-green-500/10',
            'warning': 'border-yellow-500/30 bg-yellow-500/10',
            'error': 'border-red-500/30 bg-red-500/10'
        };

        container.innerHTML = announcements.map(ann => `
            <div class="group p-4 bg-white/5 border rounded-xl transition-all hover:scale-[1.02] ${typeStyles[ann.type] || typeStyles.info}">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0" style="background: rgba(var(--theme-primary), 0.1);">
                        <i data-lucide="${iconMap[ann.icon] || 'bell'}" class="w-5 h-5" style="color: rgb(var(--theme-primary));"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between gap-2 mb-1">
                            <h5 class="font-bold text-white text-sm">${ann.title}</h5>
                            <span class="text-[10px] text-gray-500 whitespace-nowrap">${ann.date}</span>
                        </div>
                        <p class="text-xs text-gray-300 leading-relaxed">${ann.message}</p>
                    </div>
                </div>
            </div>
        `).join('');

        lucide.createIcons();
    } catch (error) {
        console.error('Failed to load announcements:', error);
    }
}

// Back button handler
function handleBackToModes() {
    console.log('Back to modes clicked');
    document.getElementById('minecraft-inject').classList.add('hidden');
    document.getElementById('injection-controls').classList.add('hidden');
    currentGameMode = null;
    lucide.createIcons();
}

// Process Selector
async function showProcessSelector() {
    const modal = document.getElementById('process-modal');
    modal.classList.remove('hidden');
    setTimeout(() => lucide.createIcons(), 100);
    await loadProcesses();
}

async function loadProcesses() {
    const listContainer = document.getElementById('process-list');
    listContainer.innerHTML = '<div class="text-center py-12 text-gray-500"><i data-lucide="loader" class="w-8 h-8 mx-auto mb-3 animate-spin"></i><p>Loading processes...</p></div>';
    lucide.createIcons();

    try {
        const response = await fetch('/api/processes');
        allProcesses = await response.json();
        
        if (allProcesses.length === 0) {
            listContainer.innerHTML = '<p class="text-center text-gray-500 py-8">No processes found</p>';
            return;
        }

        renderProcesses(allProcesses);
    } catch (error) {
        listContainer.innerHTML = '<p class="text-center text-red-400 py-8">Failed to load processes</p>';
        console.error('Failed to load processes:', error);
    }
}

function renderProcesses(processes) {
    const listContainer = document.getElementById('process-list');
    
    listContainer.innerHTML = processes.map(proc => `
        <button class="process-item group w-full p-4 rounded-xl flex items-center gap-3 text-left transition-all hover:scale-[1.01]" style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04);" onmouseover="this.style.background='rgba(255, 255, 255, 0.05)'; this.style.borderColor='rgba(255, 255, 255, 0.1)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.02)'; this.style.borderColor='rgba(255, 255, 255, 0.04)'" data-pid="${proc.pid}" data-name="${proc.name}">
            <div class="w-11 h-11 rounded-lg flex items-center justify-center flex-shrink-0" style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.08);">
                <i data-lucide="box" class="w-5 h-5 text-gray-400"></i>
            </div>
            <div class="flex-1 min-w-0">
                <p class="font-semibold text-white text-sm truncate">${proc.name}</p>
                <p class="text-xs text-gray-600 mt-0.5">PID: ${proc.pid}</p>
            </div>
            <i data-lucide="arrow-right" class="w-4 h-4 text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </button>
    `).join('');

    document.querySelectorAll('.process-item').forEach(item => {
        item.addEventListener('click', function() {
            const pid = parseInt(this.dataset.pid);
            const name = this.dataset.name;
            selectProcess(pid, name);
        });
    });

    lucide.createIcons();
}

// Process Search
if (document.getElementById('process-search')) {
    document.getElementById('process-search').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = allProcesses.filter(proc => 
            proc.name.toLowerCase().includes(searchTerm)
        );
        renderProcesses(filtered);
    });
}

function selectProcess(pid, name) {
    selectedProcess = { pid, name };
    
    document.getElementById('selected-process-name').textContent = name;
    document.getElementById('selected-process-pid').textContent = `PID: ${pid}`;
    document.getElementById('selected-process-display').classList.remove('hidden');
    document.getElementById('process-modal').classList.add('hidden');
    document.getElementById('dll-selection-section').classList.remove('hidden');
    
    updateInjectButton();
}

// Change Process Button
if (document.getElementById('change-process-btn')) {
    document.getElementById('change-process-btn').addEventListener('click', async function() {
        await showProcessSelector();
    });
}

// Close Process Modal
if (document.getElementById('close-process-modal')) {
    document.getElementById('close-process-modal').addEventListener('click', function() {
        document.getElementById('process-modal').classList.add('hidden');
    });
}

// DLL Selection
if (document.getElementById('select-dll-btn')) {
    document.getElementById('select-dll-btn').addEventListener('click', async function() {
        try {
            const dllPath = await window.pywebview.api.select_dll_file();
            
            if (dllPath) {
                selectedDll = dllPath;
                const fileName = dllPath.split('\\').pop().split('/').pop();
                
                document.getElementById('selected-dll-name').textContent = fileName;
                document.getElementById('selected-dll-path').textContent = dllPath;
                
                updateInjectButton();
            }
        } catch (error) {
            console.error('Error selecting DLL:', error);
            alert('Failed to open file dialog. Please try again.');
        }
    });
}

function updateInjectButton() {
    const btn = document.getElementById('inject-btn-fps');
    const text = document.getElementById('inject-text-fps');
    
    if (selectedProcess && selectedDll) {
        btn.disabled = false;
        btn.classList.remove('opacity-50', 'cursor-not-allowed');
        text.textContent = 'INJECT NOW';
    } else if (selectedProcess) {
        text.textContent = 'SELECT DLL FILE';
    } else {
        text.textContent = 'SELECT PROCESS & DLL';
    }
}

// FPS Injection
if (document.getElementById('inject-btn-fps')) {
    document.getElementById('inject-btn-fps').addEventListener('click', async function() {
        if (!selectedProcess || !selectedDll) return;

        const btn = this;
        const text = document.getElementById('inject-text-fps');
        const originalText = text.textContent;
        
        btn.disabled = true;
        text.textContent = 'INJECTING...';
        btn.style.transform = 'scale(0.98)';

        try {
            const response = await fetch('/inject', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    process_name: selectedProcess.name,
                    dll_path: selectedDll,
                    game_mode: 'fps'
                })
            });

            const result = await response.json();

            if (result.success) {
                text.textContent = '✓ INJECTED!';
                btn.style.background = 'linear-gradient(to bottom, #22c55e, #16a34a)';
                
                setTimeout(() => {
                    text.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                    btn.style.transform = 'scale(1)';
                }, 3000);
            } else {
                text.textContent = '✗ FAILED';
                btn.style.background = 'linear-gradient(to bottom, #ef4444, #dc2626)';
                alert(result.message || 'Injection failed');
                
                setTimeout(() => {
                    text.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                    btn.style.transform = 'scale(1)';
                }, 2000);
            }
        } catch (error) {
            console.error('Injection error:', error);
            text.textContent = '✗ ERROR';
            btn.style.background = 'linear-gradient(to bottom, #ef4444, #dc2626)';
            
            setTimeout(() => {
                text.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
                btn.style.transform = 'scale(1)';
            }, 2000);
        }
    });
}

// Minecraft Auto-Inject
if (document.getElementById('inject-btn-mc')) {
    document.getElementById('inject-btn-mc').addEventListener('click', function() {
        const btn = this;
        const text = btn.querySelector('span');
        
        text.textContent = 'INJECTING...';
        btn.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            text.textContent = '✓ INJECTED!';
            btn.style.transform = 'scale(1)';
            
            setTimeout(() => {
                text.textContent = 'INJECT';
            }, 3000);
        }, 2000);
    });
}

// Hide to Tray - Minecraft Mode
if (document.getElementById('hide-tray-btn-mc')) {
    document.getElementById('hide-tray-btn-mc').addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            if (window.pywebview) {
                window.pywebview.api.hide_to_tray();
            }
            this.style.transform = 'scale(1)';
        }, 100);
    });
}

// Self Destruct - Minecraft Mode
if (document.getElementById('self-destruct-btn-mc')) {
    document.getElementById('self-destruct-btn-mc').addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            if (confirm('⚠️ WARNING: This will permanently delete the application. Are you sure?')) {
                const btn = this;
                btn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i><span>DELETING...</span>';
                btn.classList.add('animate-pulse');
                setTimeout(() => {
                    if (window.pywebview) {
                        window.pywebview.api.close_window();
                    }
                }, 1500);
            }
            this.style.transform = 'scale(1)';
        }, 100);
    });
}

// Initialize on load
window.addEventListener('load', function() {
    console.log('Premium features loaded');
    loadAnnouncements();
    setTimeout(() => lucide.createIcons(), 500);
    
    // Setup event listeners after load to ensure elements exist
    setupEventListeners();
});

function setupEventListeners() {
    // Re-setup game mode buttons
    const minecraftBtn = document.getElementById('mode-minecraft');
    const fpsBtn = document.getElementById('mode-fps');
    
    if (minecraftBtn) {
        console.log('Setting up Minecraft button listener');
        minecraftBtn.onclick = function(e) {
            e.preventDefault();
            console.log('Minecraft clicked!');
            currentGameMode = 'minecraft';
            document.getElementById('injection-controls').classList.add('hidden');
            document.getElementById('minecraft-inject').classList.remove('hidden');
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                lucide.createIcons();
            }, 100);
        };
    }
    
    if (fpsBtn) {
        console.log('Setting up FPS button listener');
        fpsBtn.onclick = async function(e) {
            e.preventDefault();
            console.log('FPS clicked!');
            currentGameMode = 'fps';
            document.getElementById('minecraft-inject').classList.add('hidden');
            document.getElementById('injection-controls').classList.remove('hidden');
            this.style.transform = 'scale(0.95)';
            setTimeout(() => this.style.transform = 'scale(1)', 100);
            await showProcessSelector();
        };
    }
}

// Reinitialize icons when switching tabs or showing content
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.attributeName === 'class') {
            setTimeout(() => lucide.createIcons(), 100);
        }
    });
});

// Observe the minecraft-inject and injection-controls divs
const minecraftDiv = document.getElementById('minecraft-inject');
const fpsDiv = document.getElementById('injection-controls');
if (minecraftDiv) observer.observe(minecraftDiv, { attributes: true });
if (fpsDiv) observer.observe(fpsDiv, { attributes: true });

// Add modal animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes scale-in {
        from {
            transform: scale(0.9);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    .animate-scale-in {
        animation: scale-in 0.2s ease-out;
    }
    
    /* Game Mode Button Enhancements */
    .game-mode-btn {
        transform-origin: center;
        will-change: transform, box-shadow;
        cursor: pointer;
    }
    
    .game-mode-btn:hover {
        transform: scale(1.08) !important;
        box-shadow: 0 20px 40px -10px rgba(var(--theme-primary), 0.4) !important;
        z-index: 10;
    }
    
    .game-mode-btn:active {
        transform: scale(0.98) !important;
    }
`;
document.head.appendChild(style);
