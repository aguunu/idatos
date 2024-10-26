-- Create the database
-- CREATE DATABASE IF NOT EXISTS db_name;

-- Connect to the database
\connect db_name;

-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Linea
CREATE TABLE MainRoutes (
	id INT NOT NULL PRIMARY KEY,
	name TEXT
);

-- Sub-Lineas
CREATE TABLE SubRoutes (
	id INT NOT NULL PRIMARY KEY,
	route_id INT NOT NULL,
	origin TEXT NOT NULL,
	destination TEXT NOT NULL,
	path GEOMETRY(LINESTRING, 4326),
	FOREIGN KEY (route_id) REFERENCES MainRoutes(id)
);

-- Paradas
CREATE TABLE Stops (
	id INT NOT NULL PRIMARY KEY,
	point GEOMETRY(POINT, 4326)
);

-- Variantes
CREATE TABLE RouteVariants (
	id INT NOT NULL PRIMARY KEY,
	sub_route_id INT NOT NULL,
	upward BOOLEAN NOT NULL,
	FOREIGN KEY (sub_route_id) REFERENCES SubRoutes(id)
);

-- Paradas de Variantes
CREATE TABLE RouteVariantStops (
	stop_id INT NOT NULL,
	variant_id INT NOT NULL,
	ordinal INT NOT NULL,
	arrival TIME NOT NULL,
	FOREIGN KEY (stop_id) REFERENCES Stops(id),
	FOREIGN KEY (variant_id) REFERENCES RouteVariants(id)
);

-- -- Create the locations table
-- CREATE TABLE locations (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     geom GEOMETRY(POINT, 4326) -- SRID 4326 corresponds to the WGS 84 (World Geodetic System 1984)
-- );
--
-- -- Insert sample geospatial data
-- INSERT INTO locations (name, geom)
-- VALUES
-- ('Montevideo', ST_SetSRID(ST_MakePoint(34.9055, 56.1851), 4326)),
-- ('Paris', ST_SetSRID(ST_MakePoint(48.8575, 2.3514), 4326));

