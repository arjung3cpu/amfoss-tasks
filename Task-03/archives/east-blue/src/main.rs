use anyhow::Result;
use log::info;
use navnet_core::registry::{StationMetadata, StationRegistry};

fn main() -> Result<()> {
    env_logger::init();

    let mut registry = StationRegistry::new();
    info!("East Blue registry bootstrap initialized");

    registry.add_station(StationMetadata {
        station_id: "station-early".to_string(),
        hostname: "early.navnet.local".to_string(),
        protocol: "v1".to_string(),
        last_checked: "2026-07-01T00:00:00Z".to_string(),
        labels: vec![("deployment-zone".to_string(), "central".to_string())]
            .into_iter()
            .collect(),
    })?;

    info!("East Blue bootstrap completed with {} stations", registry.stations.len());
    Ok(())
}
