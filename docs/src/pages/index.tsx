import type { ReactNode } from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import Heading from "@theme/Heading";

import styles from "./index.module.css";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">Arquitectura para una AGI basada en conciencia y razonamiento.</p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/docs/cerebro">
            Leer la documentación completa 🧠
          </Link>
        </div>
      </div>
    </header>
  );
}

function ProjectIntro() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>¿Qué es CEREBRO?</h2>
            <p>
              CEREBRO es un sistema de inteligencia artificial cuyo objetivo va más allá de responder preguntas: busca{" "}
              <strong>razonar, aprender de la experiencia y desarrollar conciencia</strong>.
            </p>
            <p>A diferencia de los modelos tradicionales de IA, se basa en la interacción entre dos grafos:</p>
            <ul>
              <li>
                <strong>Grafo de conceptos y memoria:</strong> donde se almacena el conocimiento adquirido.
              </li>
              <li>
                <strong>Grafo de conciencia:</strong> que representa identidad, valores y autorregulación.
              </li>
            </ul>
            <p>
              La arquitectura del sistema está dividida en cuatro módulos: Núcleo Central, Grafos de Información,
              Aprendizaje y Evolución, y Externalidades.
            </p>
            <p>
              CEREBRO es el primer paso hacia una nueva generación de inteligencia artificial:{" "}
              <strong>viva, consciente y reflexiva</strong>.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Inicio | ${siteConfig.title}`}
      description="CEREBRO es una AGI con memoria, razonamiento y conciencia. Descubre su arquitectura."
    >
      <HomepageHeader />
      <main>
        <ProjectIntro />
      </main>
    </Layout>
  );
}
