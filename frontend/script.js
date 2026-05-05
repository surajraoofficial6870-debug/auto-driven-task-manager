// Flask API ka address (Railway par deploy ke baad URL change kar dena)
const API_BASE_URL = "http://127.0.0.1:5000/api";

function openModal(id) { document.getElementById(id).style.display = 'block'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }

// ✅ NEW: Token validation check karne ke liye
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

document.addEventListener('DOMContentLoaded', () => {
    
    // ✅ Page load par check kar: already logged in?
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userRole');
    if (token && userRole) {
        document.getElementById('authScreen').style.display = 'none';
        document.getElementById('dashboardWrapper').style.display = 'block';
        setupUIForRole(userRole);
        loadAllTasks(); // ✅ Tasks load kar startup mein
    }

    // 1. SIGNUP LOGIC (Backend se Connect)
    document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userData = {
            name: document.getElementById('regName').value.trim(),
            email: document.getElementById('regEmail').value.trim(),
            password: document.getElementById('regPass').value,
            role: document.getElementById('regRole')?.value || 'Member'
        };

        // ✅ Basic validation
        if (!userData.email.includes('@')) {
            alert("Invalid email format!");
            return;
        }
        if (userData.password.length < 6) {
            alert("Password must be at least 6 characters!");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            if (response.ok) {
                alert("Account Created! Now Login.");
                document.getElementById('signupForm').reset();
                closeModal('signupModal');
            } else {
                alert("Error: " + (data.message || "Signup failed"));
            }
        } catch (err) {
            console.error("Signup failed", err);
            alert("Network error. Check backend server!");
        }
    });

    // 2. LOGIN LOGIC (Backend Verification)
    document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const loginData = {
            email: document.getElementById('loginEmail').value.trim(),
            password: document.getElementById('loginPass').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(loginData)
            });

            const data = await response.json();
            if (response.ok) {
                // ✅ Token aur User info save karo
                localStorage.setItem('token', data.token);
                localStorage.setItem('userRole', data.user.role);
                localStorage.setItem('userName', data.user.name);
                localStorage.setItem('userId', data.user.id); // ✅ User ID bhi save kar

                alert("Welcome, " + data.user.name);
                setupUIForRole(data.user.role);
                
                document.getElementById('authScreen').style.display = 'none';
                document.getElementById('dashboardWrapper').style.display = 'block';
                closeModal('loginModal');
                
                loadAllTasks(); // ✅ Login ke baad tasks load kar
            } else {
                alert("Invalid Credentials!");
            }
        } catch (err) {
            console.error("Login failed", err);
            alert("Network error!");
        }
    });

    // 3. TASK STATUS UPDATE (KeyError Fix)
    window.updateTaskStatus = async (taskId, newStatus) => {
        try {
            const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
                method: 'PUT',
                headers: getAuthHeaders(), // ✅ Helper function use kar
                body: JSON.stringify({ status: newStatus })
            });
            if (response.ok) {
                alert("Task updated!");
                loadAllTasks(); // ✅ Reload without page refresh
            } else {
                alert("Update failed!");
            }
        } catch (err) {
            console.error("Update failed", err);
        }
    };

    // ✅ NEW: Load all tasks
    window.loadAllTasks = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/tasks`, {
                headers: getAuthHeaders()
            });
            const tasks = await response.json();
            displayTasks(tasks);
        } catch (err) {
            console.error("Failed to load tasks", err);
        }
    };

    // ✅ NEW: Display tasks on dashboard
    window.displayTasks = (tasks) => {
        const taskContainer = document.getElementById('tasksList');
        if (!taskContainer) return;
        
        taskContainer.innerHTML = tasks.map(task => `
            <div class="task-card">
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <p><strong>Status:</strong> ${task.status}</p>
                <button onclick="updateTaskStatus(${task.id}, 'completed')">Mark Complete</button>
            </div>
        `).join('');
    };
});

// ✅ Role-Based UI Control
function setupUIForRole(role) {
    const adminFeatures = document.querySelectorAll('.admin-only');
    const recruiterFeatures = document.querySelectorAll('.recruiter-only');
    
    adminFeatures.forEach(el => el.style.display = role === 'Admin' ? 'block' : 'none');
    recruiterFeatures.forEach(el => el.style.display = (role === 'Admin' || role === 'Recruiter') ? 'block' : 'none');
}

function logout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.clear();
        location.reload();
    }
}