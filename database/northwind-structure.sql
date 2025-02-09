-- -------------------------------------------------------------
-- TablePlus 6.1.2(568)
--
-- https://tableplus.com/
--
-- Database: northwind
-- Generation Time: 2567-08-27 11:56:28.4640
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."categories" (
    "category_id" int2 NOT NULL,
    "category_name" varchar(15) NOT NULL,
    "description" text,
    "picture" bytea,
    PRIMARY KEY ("category_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."customer_customer_demo" (
    "customer_id" varchar(5) NOT NULL,
    "customer_type_id" varchar(5) NOT NULL,
    PRIMARY KEY ("customer_id","customer_type_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."customer_demographics" (
    "customer_type_id" varchar(5) NOT NULL,
    "customer_desc" text,
    PRIMARY KEY ("customer_type_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."customers" (
    "customer_id" varchar(5) NOT NULL,
    "company_name" varchar(40) NOT NULL,
    "contact_name" varchar(30),
    "contact_title" varchar(30),
    "address" varchar(60),
    "city" varchar(15),
    "region" varchar(15),
    "postal_code" varchar(10),
    "country" varchar(15),
    "phone" varchar(24),
    "fax" varchar(24),
    PRIMARY KEY ("customer_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."employee_territories" (
    "employee_id" int2 NOT NULL,
    "territory_id" varchar(20) NOT NULL,
    PRIMARY KEY ("employee_id","territory_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."employees" (
    "employee_id" int2 NOT NULL,
    "last_name" varchar(20) NOT NULL,
    "first_name" varchar(10) NOT NULL,
    "title" varchar(30),
    "title_of_courtesy" varchar(25),
    "birth_date" date,
    "hire_date" date,
    "address" varchar(60),
    "city" varchar(15),
    "region" varchar(15),
    "postal_code" varchar(10),
    "country" varchar(15),
    "home_phone" varchar(24),
    "extension" varchar(4),
    "photo" bytea,
    "notes" text,
    "reports_to" int2,
    "photo_path" varchar(255),
    PRIMARY KEY ("employee_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."order_details" (
    "order_id" int2 NOT NULL,
    "product_id" int2 NOT NULL,
    "unit_price" float4 NOT NULL,
    "quantity" int2 NOT NULL,
    "discount" float4 NOT NULL,
    PRIMARY KEY ("order_id","product_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."orders" (
    "order_id" int2 NOT NULL,
    "customer_id" varchar(5),
    "employee_id" int2,
    "order_date" date,
    "required_date" date,
    "shipped_date" date,
    "ship_via" int2,
    "freight" float4,
    "ship_name" varchar(40),
    "ship_address" varchar(60),
    "ship_city" varchar(15),
    "ship_region" varchar(15),
    "ship_postal_code" varchar(10),
    "ship_country" varchar(15),
    PRIMARY KEY ("order_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."products" (
    "product_id" int2 NOT NULL,
    "product_name" varchar(40) NOT NULL,
    "supplier_id" int2,
    "category_id" int2,
    "quantity_per_unit" varchar(20),
    "unit_price" float4,
    "units_in_stock" int2,
    "units_on_order" int2,
    "reorder_level" int2,
    "discontinued" int4 NOT NULL,
    PRIMARY KEY ("product_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."region" (
    "region_id" int2 NOT NULL,
    "region_description" varchar(60) NOT NULL,
    PRIMARY KEY ("region_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."shippers" (
    "shipper_id" int2 NOT NULL,
    "company_name" varchar(40) NOT NULL,
    "phone" varchar(24),
    PRIMARY KEY ("shipper_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."suppliers" (
    "supplier_id" int2 NOT NULL,
    "company_name" varchar(40) NOT NULL,
    "contact_name" varchar(30),
    "contact_title" varchar(30),
    "address" varchar(60),
    "city" varchar(15),
    "region" varchar(15),
    "postal_code" varchar(10),
    "country" varchar(15),
    "phone" varchar(24),
    "fax" varchar(24),
    "homepage" text,
    PRIMARY KEY ("supplier_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."territories" (
    "territory_id" varchar(20) NOT NULL,
    "territory_description" varchar(60) NOT NULL,
    "region_id" int2 NOT NULL,
    PRIMARY KEY ("territory_id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."us_states" (
    "state_id" int2 NOT NULL,
    "state_name" varchar(100),
    "state_abbr" varchar(2),
    "state_region" varchar(50),
    PRIMARY KEY ("state_id")
);



-- Indices
CREATE UNIQUE INDEX pk_categories ON public.categories USING btree (category_id);
ALTER TABLE "public"."customer_customer_demo" ADD FOREIGN KEY ("customer_id") REFERENCES "public"."customers"("customer_id");
ALTER TABLE "public"."customer_customer_demo" ADD FOREIGN KEY ("customer_type_id") REFERENCES "public"."customer_demographics"("customer_type_id");


-- Indices
CREATE UNIQUE INDEX pk_customer_customer_demo ON public.customer_customer_demo USING btree (customer_id, customer_type_id);


-- Indices
CREATE UNIQUE INDEX pk_customer_demographics ON public.customer_demographics USING btree (customer_type_id);


-- Indices
CREATE UNIQUE INDEX pk_customers ON public.customers USING btree (customer_id);
ALTER TABLE "public"."employee_territories" ADD FOREIGN KEY ("employee_id") REFERENCES "public"."employees"("employee_id");
ALTER TABLE "public"."employee_territories" ADD FOREIGN KEY ("territory_id") REFERENCES "public"."territories"("territory_id");


-- Indices
CREATE UNIQUE INDEX pk_employee_territories ON public.employee_territories USING btree (employee_id, territory_id);
ALTER TABLE "public"."employees" ADD FOREIGN KEY ("reports_to") REFERENCES "public"."employees"("employee_id");


-- Indices
CREATE UNIQUE INDEX pk_employees ON public.employees USING btree (employee_id);
ALTER TABLE "public"."order_details" ADD FOREIGN KEY ("product_id") REFERENCES "public"."products"("product_id");
ALTER TABLE "public"."order_details" ADD FOREIGN KEY ("order_id") REFERENCES "public"."orders"("order_id");


-- Indices
CREATE UNIQUE INDEX pk_order_details ON public.order_details USING btree (order_id, product_id);
ALTER TABLE "public"."orders" ADD FOREIGN KEY ("customer_id") REFERENCES "public"."customers"("customer_id");
ALTER TABLE "public"."orders" ADD FOREIGN KEY ("employee_id") REFERENCES "public"."employees"("employee_id");
ALTER TABLE "public"."orders" ADD FOREIGN KEY ("ship_via") REFERENCES "public"."shippers"("shipper_id");


-- Indices
CREATE UNIQUE INDEX pk_orders ON public.orders USING btree (order_id);
ALTER TABLE "public"."products" ADD FOREIGN KEY ("category_id") REFERENCES "public"."categories"("category_id");
ALTER TABLE "public"."products" ADD FOREIGN KEY ("supplier_id") REFERENCES "public"."suppliers"("supplier_id");


-- Indices
CREATE UNIQUE INDEX pk_products ON public.products USING btree (product_id);


-- Indices
CREATE UNIQUE INDEX pk_region ON public.region USING btree (region_id);


-- Indices
CREATE UNIQUE INDEX pk_shippers ON public.shippers USING btree (shipper_id);


-- Indices
CREATE UNIQUE INDEX pk_suppliers ON public.suppliers USING btree (supplier_id);
ALTER TABLE "public"."territories" ADD FOREIGN KEY ("region_id") REFERENCES "public"."region"("region_id");


-- Indices
CREATE UNIQUE INDEX pk_territories ON public.territories USING btree (territory_id);


-- Indices
CREATE UNIQUE INDEX pk_usstates ON public.us_states USING btree (state_id);
