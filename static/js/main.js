document.addEventListener('DOMContentLoaded', () => {

    // ============== 1- Signup Validation (FR-5 - Req 14) ==========================
    const signupForm = document.getElementById('signup_form');

    const MIN_PASSWORD_LENGTH = 8;

    if (signupForm) {
        signupForm.addEventListener('submit', (event) => {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');

            let isValid = true;
            clearErrors();

            if (!nameInput || !nameInput.value.trim()) {
                showError(nameInput, 'اسم المستخدم مطلوب');
                isValid = false;
            }

            if (!emailInput || !emailInput.value.trim()) {
                showError(emailInput, 'البريد الإلكتروني مطلوب');
                isValid = false;
            } else if (!isValidEmail(emailInput.value.trim())) {
                showError(emailInput, 'صيغة البريد الإلكتروني غير صحيحة');
                isValid = false;
            }

            if (!passwordInput || !passwordInput.value.trim()) {
                showError(passwordInput, 'كلمة المرور مطلوبة');
                isValid = false;
            } else if (passwordInput.value.length < MIN_PASSWORD_LENGTH) {
                showError(passwordInput, `كلمة المرور يجب أن تكون ${MIN_PASSWORD_LENGTH} أحرف على الأقل`);
                isValid = false;
            }
            const confirmPasswordInput = document.getElementById('confirm_password');
            if (confirmPasswordInput) {
                if (!confirmPasswordInput.value.trim()) {
                    showError(confirmPasswordInput, 'تأكيد كلمة المرور مطلوب');
                    isValid = false;
                } else if (passwordInput && confirmPasswordInput.value !== passwordInput.value) {
                    showError(confirmPasswordInput, 'كلمتا المرور غير متطابقتين');
                    isValid = false;
                }
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // ============== 2- Catalog Search/Filter (FR-2 - Req 6 & Bonus Category) ==========================
    const searchInput = document.getElementById('searchbox');
    const categorySelect = document.querySelector('.Categories');
    const bookRows = document.querySelectorAll('.book-row');

    function filterBooks() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedCategory = categorySelect ? categorySelect.value.toLowerCase().trim() : 'all';

        bookRows.forEach(row => {
            const title = row.getAttribute('data-title')?.toLowerCase() || '';
            const author = row.getAttribute('data-author')?.toLowerCase() || '';
            const category = row.getAttribute('data-category')?.toLowerCase().trim() || '';

            const matchesSearch = title.includes(query) || author.includes(query);
            const matchesCategory = selectedCategory === 'all' || selectedCategory === '' || category === selectedCategory;

            row.style.display = (matchesSearch && matchesCategory) ? '' : 'none';
        });
    }

    function debounce(fn, delay = 200) {
        let timerId;
        return (...args) => {
            clearTimeout(timerId);
            timerId = setTimeout(() => fn(...args), delay);
        };
    }
    const debouncedFilterBooks = debounce(filterBooks, 200);

    if (searchInput) {
        searchInput.addEventListener('input', debouncedFilterBooks);
    }
    if (categorySelect) {
        categorySelect.addEventListener('change', filterBooks);
    }
});

// ============== 3- Helper Functions ==========================

function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

function showError(inputElement, message) {
    if (!inputElement) return;
    inputElement.classList.add('is-invalid');
    const errorContainer = document.getElementById(`${inputElement.id}-error`);
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    }
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
}