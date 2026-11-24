const API_URL = "http://127.0.0.1:8000/news/";

const newsGrid = document.getElementById("newsGrid");
const searchInput = document.getElementById("searchInput");
const categorySelect = document.getElementById("categorySelect");
const refreshBtn = document.getElementById("refreshBtn");

let searchTimer;

async function loadCategories() {
    try {
        const response = await fetch(API_URL + "categories");
        const categories = await response.json();

        categories.forEach(category => {
            const option = document.createElement("option");
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });

        document.getElementById("totalCategories").textContent =
            categories.length;

    } catch (error) {
        console.error("Category loading failed:", error);
    }
}

async function loadStats() {
    try {
        const response = await fetch(API_URL + "stats");
        const stats = await response.json();

        document.getElementById("totalArticles").textContent =
            stats.total_articles;

    } catch (error) {
        console.error("Stats loading failed:", error);
    }
}

async function loadNews() {
    newsGrid.innerHTML = '<div class="loading">Loading news...</div>';

    const category = categorySelect.value;
    const search = searchInput.value.trim();

    const params = new URLSearchParams();

    if (category) params.append("category", category);
    if (search) params.append("search", search);

    try {
        const response = await fetch(API_URL + "?" + params.toString());

        if (!response.ok) {
            throw new Error("Failed to fetch news");
        }

        const articles = await response.json();

        document.getElementById("resultText").textContent =
            `${articles.length} articles found`;

        displayNews(articles);

    } catch (error) {
        newsGrid.innerHTML =
            '<div class="no-news">Unable to load news. Please check the API server.</div>';

        console.error(error);
    }
}

function displayNews(articles) {
    newsGrid.innerHTML = "";

    if (articles.length === 0) {
        newsGrid.innerHTML =
            '<div class="no-news">No articles found.</div>';
        return;
    }

    articles.forEach(article => {
        const card = document.createElement("article");
        card.className = "news-card";

        const image = document.createElement("img");
        image.className = "news-image";
        image.alt = article.title;
        image.src = article.image || "";
        image.onerror = () => {
            image.style.display = "none";
        };

        const content = document.createElement("div");
        content.className = "news-content";

        const category = document.createElement("span");
        category.className = "news-category";
        category.textContent = article.category || "News";

        const title = document.createElement("h3");
        title.textContent = article.title;

        const description = document.createElement("p");
        description.textContent = article.description || "Read the full story from the publisher.";

        const meta = document.createElement("div");
        meta.className = "news-meta";
        meta.textContent = `${article.source || "News"} • ${article.published || ""}`;

        const link = document.createElement("a");
        link.className = "read-link";
        link.href = article.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = "Read Full Article ↗";

        content.append(category, title, description, meta, link);
        card.append(image, content);
        newsGrid.appendChild(card);
    });

    const sources = new Set(articles.map(a => a.source).filter(Boolean));
    document.getElementById("totalSources").textContent = sources.size;
}

categorySelect.addEventListener("change", loadNews);

searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadNews, 400);
});

refreshBtn.addEventListener("click", async () => {
    await loadStats();
    await loadNews();
});

loadCategories();
loadStats();
loadNews();