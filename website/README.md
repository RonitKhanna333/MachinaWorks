# AI Consultancy Website

A modern, professional Next.js website for an AI consultancy company, showcasing AI/ML solutions with business impact analysis.

## 🚀 Features

- **Modern Design**: Beautiful gradient UI with animations using Framer Motion
- **Business Impact Showcase**: Real-world examples with ROI metrics
- **Interactive Consultation Form**: Get AI recommendations instantly
- **Responsive**: Mobile-first design that works on all devices
- **Fast**: Optimized with Next.js 14 App Router
- **TypeScript**: Fully typed for better development experience

## 📦 Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **Axios** - API requests

## 🛠️ Setup

### 1. Install Dependencies

```bash
cd website
npm install
```

### 2. Configure Environment

Copy `.env.local` and add your API keys:

```bash
GROQ_API_KEY=your-groq-api-key
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### 4. Build for Production

```bash
npm run build
npm start
```

## 🔌 Backend Integration

The website includes an API route (`/app/api/consult/route.ts`) that currently returns mock data. To integrate with your Python backend:

### Option 1: Direct Python API Call

Update `/app/api/consult/route.ts`:

```typescript
const response = await fetch('http://localhost:8000/api/consult', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    problem,
    industry,
    company_size: companySize
  }),
})
const data = await response.json()
return NextResponse.json(data)
```

### Option 2: Python Backend Setup

Create a FastAPI backend in your main project:

```python
# In your main project: src/api/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot.consultant import AIConsultant
from embeddings.vector_store import VectorStore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()
consultant = AIConsultant(vector_store, llm_provider="groq")

@app.post("/api/consult")
async def consult(request: dict):
    result = consultant.suggest(
        problem=request["problem"],
        include_impact=True,
        industry=request.get("industry"),
        company_size=request.get("company_size")
    )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run the backend:
```bash
cd ..  # Back to main project
python src/api/server.py
```

## 📄 Pages

- **Home** (`/`) - Landing page with hero, features, and consultation form
- **Features** (`/features`) - Detailed feature showcase
- **Case Studies** (`/case-studies`) - Real-world implementation examples
- **About** (`/about`) - Company information

## 🎨 Customization

### Colors

Edit `tailwind.config.js` to change the color scheme:

```javascript
colors: {
  primary: { ... },  // Main brand color
  accent: { ... },   // Secondary brand color
}
```

### Content

- **Hero Section**: Edit `/app/page.tsx`
- **Features**: Edit `/components/FeatureCards.tsx`
- **Impact Examples**: Edit `/components/ImpactShowcase.tsx`
- **Navigation**: Edit `/components/Header.tsx`

### Branding

Replace the logo and brand name in:
- `/components/Header.tsx`
- `/components/Footer.tsx`
- `/app/layout.tsx` (metadata)

## 📱 Responsive Design

The website is fully responsive with breakpoints:
- Mobile: `< 768px`
- Tablet: `768px - 1024px`
- Desktop: `> 1024px`

## ⚡ Performance

- **Image Optimization**: Use Next.js `<Image>` component
- **Code Splitting**: Automatic with Next.js App Router
- **Static Generation**: Pages are pre-rendered
- **Font Optimization**: Using next/font

## 🚀 Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Other Platforms

Build and deploy the `.next` folder:

```bash
npm run build
# Deploy the .next folder to your hosting platform
```

## 📝 Environment Variables

Required for production:

```
GROQ_API_KEY=your-groq-api-key
NEXT_PUBLIC_API_URL=your-backend-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for your projects!

## 🆘 Support

- Check the Next.js documentation: https://nextjs.org/docs
- Tailwind CSS docs: https://tailwindcss.com/docs
- Framer Motion docs: https://www.framer.com/motion/

## 🎯 Next Steps

1. [ ] Add more pages (Features, Case Studies, About)
2. [ ] Integrate with Python backend
3. [ ] Add authentication for user accounts
4. [ ] Implement real-time chat consultation
5. [ ] Add blog/resources section
6. [ ] Set up analytics (Google Analytics, Plausible)
7. [ ] Add SEO optimization
8. [ ] Create email notification system
9. [ ] Add testimonials section
10. [ ] Implement A/B testing

---

Built with ❤️ using Next.js and AI
