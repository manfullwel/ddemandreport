import express from 'express';
import fetch from 'node-fetch';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Servir arquivos estáticos da pasta docs
app.use(express.static('docs'));

// Rota para proxy da demo
app.get('/api/demo', async (req, res) => {
    try {
        const response = await fetch('https://preview--demand-count-sentinel.lovable.app/');
        let text = await response.text();
        
        // Remove o badge do Lovable e outros elementos indesejados
        text = text
            .replace(/<a id="lovable-badge"[\s\S]*?<\/a>/g, '') // Remove o badge completo
            .replace(/<button id="lovable-badge-close"[\s\S]*?<\/button>/g, '') // Remove o botão de fechar
            .replace(/https:\/\/preview--demand-count-sentinel\.lovable\.app/g, '') // Remove URLs
            .replace(/lovable\.dev/g, '') // Remove referências ao Lovable
            .replace(/<meta[^>]*>/g, '') // Remove meta tags
            .replace(/<link[^>]*lovable[^>]*>/g, '') // Remove links relacionados ao Lovable
            .replace(/<!-- Lovable[\s\S]*?-->/g, ''); // Remove comentários do Lovable
        
        res.setHeader('Content-Type', 'text/html');
        res.setHeader('X-Frame-Options', 'SAMEORIGIN');
        res.setHeader('Content-Security-Policy', "frame-ancestors 'self'");
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
        res.send(text);
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).send('Erro ao carregar demo');
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor de teste rodando em http://localhost:${PORT}`);
    console.log(`Acesse http://localhost:${PORT}/demo-secure.html para ver a demo`);
});
