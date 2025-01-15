const fetch = require('node-fetch');

exports.handler = async function(event, context) {
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
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html',
        'X-Frame-Options': 'SAMEORIGIN',
        'Content-Security-Policy': "frame-ancestors 'self'",
        'Cache-Control': 'no-store, no-cache, must-revalidate'
      },
      body: text
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to load demo' })
    };
  }
}
