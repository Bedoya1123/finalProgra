-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-06-2017 a las 03:10:38
-- Versión del servidor: 5.6.21
-- Versión de PHP: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `minutos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE IF NOT EXISTS `factura` (
`id_factura` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(36) NOT NULL,
  `cedula` varchar(50) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `total` float NOT NULL,
  `puntos` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `factura`
--

INSERT INTO `factura` (`id_factura`, `fecha`, `id_usuario`, `nombre`, `apellido`, `cedula`, `direccion`, `telefono`, `total`, `puntos`) VALUES
(28, '2017-06-15', 27, 'Cristian', 'Bedoya', '123456', '', '', 39000, 7),
(29, '2017-06-15', 27, 'Cristian', 'Bedoya', '123456', '', '', 146500, 29),
(30, '2017-06-15', 27, 'Cristian', 'Bedoya', '123456', '', '', 6500, 1),
(31, '2017-06-15', 27, 'Cristian', 'Bedoya', '123456', '', '', 31500, 6),
(32, '2017-06-15', 27, 'Cristian', 'Bedoya', '123456', '', '', 25000, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquete`
--

CREATE TABLE IF NOT EXISTS `paquete` (
`id_paquete` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `precio` float DEFAULT NULL,
  `existencia` int(4) DEFAULT NULL,
  `minimo` int(11) DEFAULT NULL,
  `puntos` int(5) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `paquete`
--

INSERT INTO `paquete` (`id_paquete`, `nombre`, `precio`, `existencia`, `minimo`, `puntos`) VALUES
(2, 'Paq Claro 50 min', 6500, 43, 5, 3),
(3, 'Paq tigo 1000 min', 25000, 92, 10, 10),
(4, 'Paq movistar 200 min', 14000, 47, 5, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puntos`
--

CREATE TABLE IF NOT EXISTS `puntos` (
  `valorpunto` int(11) NOT NULL,
  `tasacambio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `puntos`
--

INSERT INTO `puntos` (`valorpunto`, `tasacambio`) VALUES
(50, 500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_usuario`
--

CREATE TABLE IF NOT EXISTS `tipo_usuario` (
`id_tipo` int(11) NOT NULL,
  `descripcion` varchar(50) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `tipo_usuario`
--

INSERT INTO `tipo_usuario` (`id_tipo`, `descripcion`) VALUES
(1, 'usuario cliente'),
(2, 'usuario administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tmp_detalle`
--

CREATE TABLE IF NOT EXISTS `tmp_detalle` (
  `id_usuario` int(11) NOT NULL,
  `id_paquete` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cantidad` int(4) NOT NULL,
  `precio` float NOT NULL,
  `subtotal` float NOT NULL,
  `id_factura` int(11) NOT NULL,
  `grabado` int(1) NOT NULL DEFAULT '0',
  `puntos` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `tmp_detalle`
--

INSERT INTO `tmp_detalle` (`id_usuario`, `id_paquete`, `nombre`, `cantidad`, `precio`, `subtotal`, `id_factura`, `grabado`, `puntos`) VALUES
(27, 3, 'Paq tigo 1000 min', 1, 25000, 25000, 28, 1, 0),
(27, 4, 'Paq movistar 200 min', 1, 14000, 14000, 28, 1, 0),
(27, 2, 'Paq Claro 50 min', 5, 6500, 32500, 29, 1, 15),
(27, 4, 'Paq movistar 200 min', 1, 14000, 14000, 29, 1, 5),
(27, 3, 'Paq tigo 1000 min', 4, 25000, 100000, 29, 1, 40),
(41, 3, 'Paq tigo 1000 min', 2, 25000, 50000, 0, 0, 20),
(27, 2, 'Paq Claro 50 min', 1, 6500, 6500, 30, 1, 3),
(27, 3, 'Paq tigo 1000 min', 1, 25000, 25000, 31, 1, 10),
(27, 2, 'Paq Claro 50 min', 1, 6500, 6500, 31, 1, 3),
(27, 3, 'Paq tigo 1000 min', 1, 25000, 25000, 32, 1, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE IF NOT EXISTS `usuario` (
  `nombre` varchar(20) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `cedula` varchar(50) NOT NULL,
  `clave` varchar(20) DEFAULT NULL,
`id_usuario` int(11) NOT NULL,
  `id_tipo` int(11) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `puntos` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`nombre`, `apellido`, `cedula`, `clave`, `id_usuario`, `id_tipo`, `email`, `direccion`, `telefono`, `puntos`) VALUES
('leidy', 'hernandez', '', 'oqiwr6nu', 1, 2, 'ladyvivi_17@hotmail.com', '', '', 0),
('Cristian', 'Bedoya', '123456', '1234', 27, 1, 'cristian@hotmail.com', '', '', 55),
('Ramon', 'Quebrada ', '', '1234', 32, 1, 'rfquebrada@hotmail.com', '', '', 0),
('fredy', 'cotecnova', '', '1234', 33, 1, 'rfq@gmail.com', '', '', 0),
('ramon fredy', 'asdsdf', '', 'vdfggd', 34, 1, 'fghgh', '', '', 0),
('sdvdfvb', 'fdbgfbngbgfn', '', 'nmh,m,', 35, 1, 'mj,,j.', '', '', 0),
(' vvb ', 'nb nm ', '', 'mn', 36, 2, 'm,', '', '', 0),
(' vvb ', 'nb nm ', '', 'mn', 37, 2, 'm,', '', '', 0),
(' vvb ', 'nb nm ', '', 'mn', 38, 2, 'm,', '', '', 0),
('lccdfv', 'fbgn', '', 'fnbm', 39, 1, 'vnbm', '', '', 0),
('sxcsacc', 'sdcfsfv', '', 'xcxscv', 40, 2, 'aasdsffd', '', '', 0),
('pepe', 'pipa', '', '1234', 41, 1, 'pepe@hotmail.com', '', '', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
 ADD PRIMARY KEY (`id_factura`);

--
-- Indices de la tabla `paquete`
--
ALTER TABLE `paquete`
 ADD PRIMARY KEY (`id_paquete`);

--
-- Indices de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
 ADD PRIMARY KEY (`id_tipo`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
 ADD PRIMARY KEY (`id_usuario`), ADD KEY `id_tipo` (`id_tipo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
MODIFY `id_factura` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=33;
--
-- AUTO_INCREMENT de la tabla `paquete`
--
ALTER TABLE `paquete`
MODIFY `id_paquete` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
MODIFY `id_tipo` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=42;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_usuario` (`id_tipo`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
