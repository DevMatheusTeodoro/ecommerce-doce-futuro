CREATE DATABASE doce_futuro;
USE doce_futuro;

-- 1. Tabelas independentes primeiro (sem Foreign Keys)
CREATE TABLE IF NOT EXISTS `cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `produto` (
  `id_cupcake` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text,
  `preco` decimal(10,2) NOT NULL,
  `estoque` int NOT NULL,
  `imagem` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_cupcake`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2. Tabela pedido (depende de cliente)
CREATE TABLE IF NOT EXISTS `pedido` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `data_pedido` datetime DEFAULT CURRENT_TIMESTAMP,
  `status_pedido` varchar(50) DEFAULT 'Aguardando Pagamento',
  `valor_total` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Preparando',
  `pagamento` varchar(50) DEFAULT NULL,
  `cep` varchar(10) DEFAULT NULL,
  `logradouro` varchar(150) DEFAULT NULL,
  `numero` varchar(20) DEFAULT NULL,
  `complemento` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3. Tabelas dependentes de pedido e produto
CREATE TABLE IF NOT EXISTS `entrega` (
  `id_entrega` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `cep` varchar(15) NOT NULL,
  `logradouro` varchar(255) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `codigo_rastreio` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_entrega`),
  UNIQUE KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `entrega_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `itempedido` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `id_cupcake` int NOT NULL,
  `quantidade` int NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_item`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_cupcake` (`id_cupcake`),
  CONSTRAINT `itempedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE CASCADE,
  CONSTRAINT `itempedido_ibfk_2` FOREIGN KEY (`id_cupcake`) REFERENCES `produto` (`id_cupcake`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `pagamento` (
  `id_pagamento` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `metodo_pagamento` varchar(50) NOT NULL,
  `status_pagamento` varchar(50) DEFAULT 'Processando',
  `data_pagamento` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pagamento`),
  UNIQUE KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `pagamento_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4. Popular a vitrine com os 4 cupcakes iniciais
INSERT INTO `produto` (`nome`, `descricao`, `preco`, `estoque`, `imagem`) VALUES
('Cupcake Chocolate Belga', 'Massa fofinha de cacau 70% com cobertura cremosa de ganache de chocolate belga.', 12.90, 20, 'belga.png'),
('Cupcake Torta de Limão', 'Massa cítrica suave recheada com creme de limão siciliano e merengue maçaricado.', 11.50, 20, 'lemon.png'),
('Cupcake Leite Ninho com Nutella', 'Massa branca tradicional com recheio generoso de Nutella e cobertura de Leite Ninho.', 13.50, 20, 'ninho.png'),
('Cupcake Red Velvet', 'Clássico veludo vermelho com cobertura suave e aveludada de cream cheese.', 12.90, 20, 'red.png');