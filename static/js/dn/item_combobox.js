(function (window) {
    let itemOptions = [];

    function readOptionsFromPage() {
        const el = document.getElementById('item-descriptions-data');
        if (!el) {
            return [];
        }
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            return [];
        }
    }

    itemOptions = readOptionsFromPage();

    window.setItemDescriptionOptions = function (items) {
        itemOptions = Array.isArray(items) ? items : [];
    };

    function filterItems(query) {
        const q = (query || '').trim().toLowerCase();
        if (!q) {
            return itemOptions.slice(0, 40);
        }
        return itemOptions
            .filter(function (name) {
                return name.toLowerCase().includes(q);
            })
            .slice(0, 40);
    }

    function initItemDescriptionCombobox(input) {
        if (!input || input.dataset.comboboxInit === '1') {
            return;
        }
        input.dataset.comboboxInit = '1';
        input.removeAttribute('list');

        let wrapper = input.closest('.item-description-combobox');
        if (!wrapper) {
            wrapper = document.createElement('div');
            wrapper.className = 'item-description-combobox';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
        }

        let list = wrapper.querySelector('.item-description-suggestions');
        if (!list) {
            list = document.createElement('ul');
            list.className = 'item-description-suggestions';
            list.hidden = true;
            wrapper.appendChild(list);
        }

        function hideSuggestions() {
            list.hidden = true;
            list.innerHTML = '';
        }

        function showSuggestions() {
            const matches = filterItems(input.value);
            list.innerHTML = '';
            if (!matches.length) {
                hideSuggestions();
                return;
            }
            matches.forEach(function (text) {
                const li = document.createElement('li');
                li.textContent = text;
                li.addEventListener('mousedown', function (e) {
                    e.preventDefault();
                    input.value = text;
                    hideSuggestions();
                });
                list.appendChild(li);
            });
            list.hidden = false;
        }

        input.addEventListener('input', showSuggestions);
        input.addEventListener('focus', showSuggestions);
        input.addEventListener('blur', function () {
            window.setTimeout(hideSuggestions, 150);
        });
    }

    window.initItemDescriptionComboboxes = function (root) {
        (root || document).querySelectorAll('.item-description-input').forEach(initItemDescriptionCombobox);
    };

    document.addEventListener('DOMContentLoaded', function () {
        window.initItemDescriptionComboboxes();
    });
})(window);
