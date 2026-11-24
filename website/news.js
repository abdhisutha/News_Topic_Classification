
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
    },
    {
        title: "The Future of Artificial Intelligence",
        category: "Technology",
        description: "New AI models are improving productivity, decision-making, and creative problem-solving across industries.",
        source: "AI News",
        published: "Today",
        url: "https://techcrunch.com/category/artificial-intelligence/",
        image: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600"
    },
    {
        title: "Major Football Championships",
        category: "Sports",
        description: "Teams worldwide are preparing for major tournaments with intense competition and exciting performances.",
        source: "ESPN",
        published: "Today",
        url: "https://www.espn.com/football/",
        image: "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=600"
    },
    {
        title: "Stock Markets Respond to Economic Changes",
        category: "Business",
        description: "Investors are watching market movements, economic policies, and corporate earnings closely.",
        source: "Reuters",
        published: "Today",
        url: "https://www.reuters.com/markets/",
        image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600"
    },
    {
        title: "Breakthroughs in Medical Research",
        category: "Science",
        description: "Medical researchers are exploring innovative treatments and technologies to improve healthcare.",
        source: "Science Daily",
        published: "Today",
        url: "https://www.sciencedaily.com/news/health_medicine/",
        image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600"
    },
    {
        title: "International Cooperation and Diplomacy",
        category: "World",
        description: "International organizations and nations continue discussions on security, trade, and cooperation.",
        source: "BBC News",
        published: "Today",
        url: "https://www.bbc.com/news/world",
        image: "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=600"
    },
    {
        title: "Cybersecurity in the Digital Age",
        category: "Technology",
        description: "Organizations are strengthening cybersecurity systems to protect data and digital infrastructure.",
        source: "Tech News",
        published: "Today",
        url: "https://www.wired.com/",
        image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600"
    },
    {
        title: "India's Rising Sporting Talent",
        category: "Sports",
        description: "Young Indian athletes are gaining recognition through their performances in national and international events.",
        source: "Sports News",
        published: "Today",
        url: "https://www.espn.com",
        image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600"
    },
    {
        title: "Global Trade and Industry Growth",
        category: "Business",
        description: "Businesses are adapting to new trade opportunities, supply chains, and changing consumer demand.",
        source: "Business News",
        published: "Today",
        url: "https://www.reuters.com/business/",
        image: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600"
    },
    {
        title: "Exploring Space and the Universe",
        category: "Science",
        description: "Space missions and astronomical research are expanding our understanding of the universe.",
        source: "Science News",
        published: "Today",
        url: "https://www.nasa.gov/",
        image: "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600"
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
            article.description.toLowerCase().includes(search) ||
            article.category.toLowerCase().includes(search) ||
            article.source.toLowerCase().includes(search);

        return matchesCategory && matchesSearch;
    });

    document.getElementById("resultText").textContent =
        `${filteredNews.length} articles found`;

    displayNews(filteredNews);
}

function displayNews(articles) {
    newsGrid.innerHTML = "";

    if (articles.length === 0) {
        newsGrid.innerHTML = `
            <div class="no-news">
                <h3>No articles found</h3>
                <p>Try searching for another keyword or category.</p>
            </div>
        `;
        document.getElementById("totalSources").textContent = 0;
        return;
    }

    articles.forEach(article => {
        const card = document.createElement("article");
        card.className = "news-card";

        const image = document.createElement("img");
        image.className = "news-image";
        image.src = article.image;
        image.alt = article.title;
        image.loading = "lazy";
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
