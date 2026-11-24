
const sampleNews = [
    {
        title: "Artificial Intelligence is Transforming Technology",
        category: "Technology",
        description: "AI is rapidly changing industries through automation, intelligent systems, and advanced data analysis.",
        source: "Tech News",
        published: "Today",
        url: "https://www.bbc.com/news/technology",
        image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600"
    },
    {
        title: "India Advances in Global Sports",
        category: "Sports",
        description: "Indian athletes continue to make their mark in international sporting competitions.",
        source: "Sports News",
        published: "Today",
        url: "https://www.espn.com",
        image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600"
    },
    {
        title: "Global Markets and Business Trends",
        category: "Business",
        description: "Global markets are adapting to changing economic conditions and new investment opportunities.",
        source: "Business News",
        published: "Today",
        url: "https://www.reuters.com/business/",
        image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600"
    },
    {
        title: "Scientific Discoveries Shape the Future",
        category: "Science",
        description: "Researchers continue to explore new discoveries in science, innovation, and emerging technologies.",
        source: "Science News",
        published: "Today",
        url: "https://www.sciencedaily.com",
        image: "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600"
    },
    {
        title: "World Leaders Discuss Global Challenges",
        category: "World",
        description: "Countries are working together to address international challenges and strengthen cooperation.",
        source: "World News",
        published: "Today",
        url: "https://www.bbc.com/news/world",
        image: "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600"
    },
    {
        title: "New Innovations in Digital Technology",
        category: "Technology",
        description: "Emerging digital technologies are reshaping how people work, communicate, and access information.",
        source: "Tech News",
        published: "Today",
        url: "https://techcrunch.com",
        image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600"
    }
];

const newsGrid = document.getElementById("newsGrid");
const searchInput = document.getElementById("searchInput");
const categorySelect = document.getElementById("categorySelect");
const refreshBtn = document.getElementById("refreshBtn");

const categories = ["All", "Technology", "Sports", "Business", "Science", "World"];

categorySelect.innerHTML = '<option value="">All Categories</option>';

categories.slice(1).forEach(category => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
});

document.getElementById("totalCategories").textContent = categories.length - 1;
document.getElementById("totalArticles").textContent = sampleNews.length;

function loadNews() {
    const category = categorySelect.value;
    const search = searchInput.value.trim().toLowerCase();

    const filteredNews = sampleNews.filter(article => {
        const matchesCategory = !category || article.category === category;
        const matchesSearch =
            !search ||
            article.title.toLowerCase().includes(search) ||
            article.description.toLowerCase().includes(search);

        return matchesCategory && matchesSearch;
    });

    document.getElementById("resultText").textContent =
        `${filteredNews.length} articles found`;

    displayNews(filteredNews);
}

function displayNews(articles) {
    newsGrid.innerHTML = "";

    articles.forEach(article => {
        const card = document.createElement("article");
        card.className = "news-card";

        const image = document.createElement("img");
        image.className = "news-image";
        image.src = article.image;
        image.alt = article.title;
        image.onerror = () => image.style.display = "none";

        const content = document.createElement("div");
        content.className = "news-content";

        const category = document.createElement("span");
        category.className = "news-category";
        category.textContent = article.category;

        const title = document.createElement("h3");
        title.textContent = article.title;

        const description = document.createElement("p");
        description.textContent = article.description;

        const meta = document.createElement("div");
        meta.className = "news-meta";
        meta.textContent = `${article.source} • ${article.published}`;

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

    document.getElementById("totalSources").textContent =
        new Set(articles.map(article => article.source)).size;
}

categorySelect.addEventListener("change", loadNews);

searchInput.addEventListener("input", loadNews);

refreshBtn.addEventListener("click", loadNews);

loadNews();
