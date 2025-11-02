/**
 * Tailwind Masonry Photo Gallery
 * Creates a masonry layout matching the pattern:
 * Left block: small-small-large
 * Right block: large-small-small
 * Repeat...
 */

async function loadGallery() {
    const container = document.getElementById('gallery-container');

    try {
        console.log('🔍 Fetching gallery.json...');

        const response = await fetch('/images/lab/gallery.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        let files = await response.json();
        console.log(`✅ Loaded ${files.length} files from JSON`);

        // Sort by modification time descending (newest first)
        files.sort((a, b) => b.time - a.time);

        // Filter image files
        const imageFiles = files.filter(file =>
            /\.(jpe?g|png|gif|webp)$/i.test(file.name)
        );

        console.log(`🖼️ Found ${imageFiles.length} image files`);

        if (imageFiles.length === 0) {
            container.innerHTML = '<p class="text-center py-10 text-gray-500">No images found in gallery</p>';
            return;
        }

        // Create main wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'flex flex-wrap w-full';

        let currentIndex = 0;

        // Build masonry blocks
        while (currentIndex < imageFiles.length) {
            // Left column block (50% width)
            const leftBlock = createMasonryBlock('left', imageFiles, currentIndex);
            if (leftBlock.imagesUsed > 0) {
                wrapper.appendChild(leftBlock.element);
                currentIndex += leftBlock.imagesUsed;
            }

            // Right column block (50% width)
            if (currentIndex < imageFiles.length) {
                const rightBlock = createMasonryBlock('right', imageFiles, currentIndex);
                if (rightBlock.imagesUsed > 0) {
                    wrapper.appendChild(rightBlock.element);
                    currentIndex += rightBlock.imagesUsed;
                }
            }
        }

        // Clear container and add gallery
        container.innerHTML = '';
        container.appendChild(wrapper);

        // Initialize Fancybox if available
        if (typeof Fancybox !== 'undefined') {
            Fancybox.bind("[data-fancybox='gallery']", {});
        }

        console.log(`🎉 Gallery loaded: ${imageFiles.length} images in masonry layout`);

    } catch (err) {
        console.error('Error loading gallery:', err);
        container.innerHTML = `
            <div class="text-center py-10 text-red-600 dark:text-red-400">
                <strong>Error loading gallery:</strong><br>
                ${err.message}<br><br>
                <small>Check console for details</small>
            </div>
        `;
    }
}

/**
 * Creates a masonry block with specific pattern
 * @param {string} type - 'left' or 'right' determines the pattern
 * @param {Array} imageFiles - Array of image file objects
 * @param {number} startIndex - Starting index in imageFiles array
 * @returns {Object} - { element: HTMLElement, imagesUsed: number }
 */
function createMasonryBlock(type, imageFiles, startIndex) {
    const blockDiv = document.createElement('div');
    blockDiv.className = 'flex w-full md:w-1/2 flex-wrap';

    let imagesUsed = 0;

    if (type === 'left') {
        // Pattern: small (50%) + small (50%) on top, large (100%) on bottom
        // Row 1: Two small images side by side
        if (imageFiles[startIndex]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex], 'w-full md:w-1/2'));
            imagesUsed++;
        }
        if (imageFiles[startIndex + 1]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 1], 'w-full md:w-1/2'));
            imagesUsed++;
        }
        // Row 2: One large image
        if (imageFiles[startIndex + 2]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 2], 'w-full'));
            imagesUsed++;
        }
    } else {
        // Pattern: large (100%) on top, small (50%) + small (50%) on bottom
        // Row 1: One large image
        if (imageFiles[startIndex]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex], 'w-full'));
            imagesUsed++;
        }
        // Row 2: Two small images side by side
        if (imageFiles[startIndex + 1]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 1], 'w-full md:w-1/2'));
            imagesUsed++;
        }
        if (imageFiles[startIndex + 2]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 2], 'w-full md:w-1/2'));
            imagesUsed++;
        }
    }

    return { element: blockDiv, imagesUsed };
}

/**
 * Creates an image wrapper with proper Tailwind classes and structure
 * @param {Object} file - Image file object with name, date, etc.
 * @param {string} widthClass - Tailwind width class (e.g., 'w-1/2', 'w-full')
 * @returns {HTMLElement} - Complete wrapper div element
 */
function createImageWrapper(file, widthClass) {
    // Outer wrapper
    const wrapper = document.createElement('div');
    wrapper.className = `${widthClass} p-1`;

    // Inner overflow container
    const innerDiv = document.createElement('div');
    innerDiv.className = 'overflow-hidden h-full w-full';

    // Link for lightbox
    const link = document.createElement('a');
    link.href = `/images/lab/${file.name}`;
    link.setAttribute('data-fancybox', 'gallery');

    // Add caption if date is available
    if (file.date) {
        const dateStr = new Date(file.date).toLocaleDateString();
        link.setAttribute('data-caption', `${file.name} (${dateStr})`);
    } else {
        link.setAttribute('data-caption', file.name);
    }

    // Image element
    const img = document.createElement('img');
    img.src = `/images/lab/${file.name}`;
    img.alt = file.name;
    img.className = 'block h-full w-full object-cover object-center opacity-0 animate-fade-in transition duration-500 transform scale-100 hover:scale-110';

    // Store metadata
    if (file.date) {
        img.dataset.date = file.date;
    }
    if (file.time) {
        img.dataset.time = file.time;
    }

    // Build structure
    link.appendChild(img);
    innerDiv.appendChild(link);
    wrapper.appendChild(innerDiv);

    return wrapper;
}

// Run on page load
document.addEventListener('DOMContentLoaded', loadGallery);



async function loadGallery() {
    const container = document.getElementById('gallery-container');
    const loading = document.getElementById('loading');

    try {
        // Fetch gallery.json
        const response = await fetch('/images/lab/gallery.json');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        let files = await response.json();

        // Sort by modification time descending (newest first)
        files.sort((a, b) => b.time - a.time);

        // Filter image files
        const imageFiles = files.filter(file =>
            /\.(jpe?g|png|gif|webp)$/i.test(file.name)
        );

        if (imageFiles.length === 0) {
            container.innerHTML = '<p class="text-center py-10">No images found</p>';
            return;
        }

        // Remove loading message
        loading.remove();

        // Split images into groups for masonry layout
        // This creates the alternating pattern like the example
        const wrapper = document.createElement('div');
        wrapper.className = 'flex flex-wrap w-full';

        let currentIndex = 0;

        // Create masonry blocks in pattern: 
        // Block 1 (left, 50%): small-small-large pattern
        // Block 2 (right, 50%): large-small-small pattern
        // Repeat...

        while (currentIndex < imageFiles.length) {
            // Left column block (50% width)
            const leftBlock = createMasonryBlock('left', imageFiles, currentIndex);
            if (leftBlock.imagesUsed > 0) {
                wrapper.appendChild(leftBlock.element);
                currentIndex += leftBlock.imagesUsed;
            }

            // Right column block (50% width)
            if (currentIndex < imageFiles.length) {
                const rightBlock = createMasonryBlock('right', imageFiles, currentIndex);
                if (rightBlock.imagesUsed > 0) {
                    wrapper.appendChild(rightBlock.element);
                    currentIndex += rightBlock.imagesUsed;
                }
            }
        }

        container.appendChild(wrapper);

        // Initialize Fancybox
        Fancybox.bind("[data-fancybox='gallery']", {});

        console.log(`✅ Gallery loaded: ${imageFiles.length} images`);

    } catch (err) {
        console.error('Error loading gallery:', err);
        container.innerHTML = `
                    <div class="text-center py-10 text-red-600">
                        <p>Error loading gallery: ${err.message}</p>
                        <p class="text-sm mt-2">Check console for details</p>
                    </div>
                `;
    }
}

function createMasonryBlock(type, imageFiles, startIndex) {
    const blockDiv = document.createElement('div');
    blockDiv.className = 'flex w-full md:w-1/2 flex-wrap';

    let imagesUsed = 0;

    if (type === 'left') {
        // Pattern: small (25%) + small (25%) + large (50%)
        // Row 1: Two small images side by side
        if (imageFiles[startIndex]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex], 'w-1/2'));
            imagesUsed++;
        }
        if (imageFiles[startIndex + 1]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 1], 'w-1/2'));
            imagesUsed++;
        }
        // Row 2: One large image
        if (imageFiles[startIndex + 2]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 2], 'w-full'));
            imagesUsed++;
        }
    } else {
        // Pattern: large (50%) + small (25%) + small (25%)
        // Row 1: One large image
        if (imageFiles[startIndex]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex], 'w-full'));
            imagesUsed++;
        }
        // Row 2: Two small images side by side
        if (imageFiles[startIndex + 1]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 1], 'w-1/2'));
            imagesUsed++;
        }
        if (imageFiles[startIndex + 2]) {
            blockDiv.appendChild(createImageWrapper(imageFiles[startIndex + 2], 'w-1/2'));
            imagesUsed++;
        }
    }

    return { element: blockDiv, imagesUsed };
}

function createImageWrapper(file, widthClass) {
    const wrapper = document.createElement('div');
    wrapper.className = `${widthClass} md:${widthClass} p-1`;

    const innerDiv = document.createElement('div');
    innerDiv.className = 'overflow-hidden h-full w-full';

    const link = document.createElement('a');
    link.href = `/images/lab/${file.name}`;
    link.setAttribute('data-fancybox', 'gallery');
    link.setAttribute('data-caption', file.name);

    const img = document.createElement('img');
    img.src = `/images/lab/${file.name}`;
    img.alt = file.name;
    img.className = 'block h-full w-full object-cover object-center gallery-image transform scale-100';

    // Add date info if available
    if (file.date) {
        img.dataset.date = file.date;
    }

    link.appendChild(img);
    innerDiv.appendChild(link);
    wrapper.appendChild(innerDiv);

    return wrapper;
}

// Load gallery on page load
document.addEventListener('DOMContentLoaded', loadGallery);