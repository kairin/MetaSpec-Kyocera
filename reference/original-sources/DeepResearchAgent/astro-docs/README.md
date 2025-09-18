# DeepResearchAgent Documentation Site

Modern documentation site built with Astro, Tailwind CSS, and shadcn/ui components.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🎨 Design System

This site uses:
- **[Astro](https://astro.build/)** - Static site generator
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[shadcn/ui](https://ui.shadcn.com/)** - Re-usable components built using Radix UI and Tailwind CSS
- **[Lucide React](https://lucide.dev/)** - Beautiful & consistent icons

## 📁 Project Structure

```
src/
├── components/
│   └── ui/                 # shadcn/ui components
├── layouts/
│   └── Layout.astro        # Main layout component
├── pages/
│   ├── index.astro         # Homepage
│   ├── quick-start.astro   # Quick start guide
│   └── emergency-recovery.astro # Emergency procedures
├── styles/
│   └── globals.css         # Global styles and Tailwind setup
└── lib/
    └── utils.ts            # Utility functions
```

## 🎯 Key Features

- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Emergency Recovery** - Prominently featured emergency procedures for terminal issues
- **Modern UI Components** - Consistent design system using shadcn/ui
- **Fast Performance** - Static generation with Astro
- **Developer Experience** - TypeScript support and path mapping

## 🚨 Emergency Recovery

The site prominently features emergency recovery procedures for terminal mouse tracking issues. The emergency recovery page is accessible at `/emergency-recovery` and includes:

- Quick reference card for immediate action
- Step-by-step recovery methods
- Root cause analysis
- Prevention measures
- Technical details

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 📝 Content Management

Pages are created as `.astro` files in the `src/pages/` directory. The site uses:

- **Component-based architecture** with reusable UI components
- **TypeScript support** for type safety
- **CSS-in-JS** through Tailwind CSS classes
- **Modern build tools** with Vite integration

## 🛠️ Development

### Adding New Pages

1. Create a new `.astro` file in `src/pages/`
2. Import the `Layout` component
3. Use shadcn/ui components for consistent styling
4. Import global CSS with `@import '../styles/globals.css'`

### Using UI Components

```astro
---
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
---

<Card>
  <CardHeader>
    <CardTitle>Example Card</CardTitle>
  </CardHeader>
  <CardContent>
    <Button>Click me</Button>
  </CardContent>
</Card>
```

## 🔗 Related

- [Main DeepResearchAgent Repository](../README.md)
- [Emergency Recovery Guide](src/pages/emergency-recovery.astro)
- [File Organization Documentation](../docs/FILE_ORGANIZATION.md)
