<script>
  import { onMount } from "svelte";
  import maplibregl from "maplibre-gl";
  import "maplibre-gl/dist/maplibre-gl.css";
  import { selectedLSG, selectedDistrict, mapReady } from "$lib/store.js";

  let mapContainer;
  let map;

  // React to LSG selection
  $: if (map && $selectedLSG) {
    let lat, lon;

    if ($selectedLSG.centroid && Array.isArray($selectedLSG.centroid)) {
      [lon, lat] = $selectedLSG.centroid;
    } else {
      lat = parseFloat($selectedLSG.lat || $selectedLSG.centroid_lat);
      lon = parseFloat($selectedLSG.lon || $selectedLSG.centroid_lon);
    }

    if (lat && lon) {
      map.flyTo({
        center: [lon, lat],
        zoom: 12,
        essential: true,
      });
    }
  }

  // React to District selection
  $: if (map && $selectedDistrict) {
    // Find district center from the districts source or hardcode for speed
    // Here we'll just filter the LSGs but a better way is to have district centroids
    const districtCenters = {
      Alappuzha: [76.33, 9.49],
      Ernakulam: [76.27, 9.98],
      Idukki: [76.99, 9.85],
      Kannur: [75.37, 11.87],
      Kasaragod: [75.0, 12.5],
      Kollam: [76.59, 8.89],
      Kottayam: [76.52, 9.59],
      Kozhikode: [75.78, 11.25],
      Malappuram: [76.07, 11.07],
      Palakkad: [76.65, 10.78],
      Pathanamthitta: [76.79, 9.26],
      Thiruvananthapuram: [76.94, 8.52],
      Thrissur: [76.21, 10.52],
      Wayanad: [76.08, 11.69],
    };

    const center = districtCenters[$selectedDistrict];
    if (center) {
      map.flyTo({
        center: [center[0], center[1]],
        zoom: 9.5,
        essential: true,
      });
    }
  }

  onMount(async () => {
    map = new maplibregl.Map({
      container: mapContainer,
      style:
        "https://tiles.basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [76.5, 10.5], // Center of Kerala
      zoom: 7,
      antialias: true,
    });

    map.on("load", async () => {
      // Add Districts Layer
      map.addSource("districts", {
        type: "geojson",
        data: "/data/kerala_districts.geojson",
      });

      map.addLayer({
        id: "districts-line",
        type: "line",
        source: "districts",
        paint: {
          "line-color": "#0d9488",
          "line-width": 1.5,
          "line-opacity": 0.5,
        },
      });

      // Add LSGs Layer
      map.addSource("lsgs", {
        type: "geojson",
        data: "/data/kerala_lsg_final.geojson",
        generateId: true,
      });

      map.addLayer({
        id: "lsgs-fill",
        type: "fill",
        source: "lsgs",
        paint: {
          "fill-color": [
            "match",
            ["get", "lsg_type"],
            "municipal corporation",
            "#ec4899", // Pink 500
            "municipality",
            "#f59e0b", // Amber 500
            "gram panchayat",
            "#10b981", // Emerald 500
            "#94a3b8", // Slate 400 (default)
          ],
          "fill-opacity": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            0.6,
            0.2,
          ],
        },
      });

      map.addLayer({
        id: "lsgs-line",
        type: "line",
        source: "lsgs",
        paint: {
          "line-color": [
            "match",
            ["get", "lsg_type"],
            "municipal corporation",
            "#fbcfe8",
            "municipality",
            "#fde68a",
            "gram panchayat",
            "#a7f3d0",
            "#f1f5f9",
          ],
          "line-width": 0.5,
          "line-opacity": 0.4,
        },
      });

      // Add Mahe Boundary (Union Territory)
      map.addSource("mahe", {
        type: "geojson",
        data: "/data/mahe_boundary.geojson",
      });

      map.addLayer({
        id: "mahe-fill",
        type: "fill",
        source: "mahe",
        paint: {
          "fill-color": "#475569", // slate-600
          "fill-opacity": 0.4,
        },
      });

      map.addLayer({
        id: "mahe-line",
        type: "line",
        source: "mahe",
        paint: {
          "line-color": "#0ea5e9", // sky-500
          "line-width": 2,
          "line-dasharray": [2, 1],
        },
      });

      // Tooltip logic
      const tooltip = document.getElementById("map-tooltip");

      // Interactive behaviors
      let hoveredId = null;

      map.on("mousemove", "lsgs-fill", (e) => {
        if (e.features.length > 0) {
          if (hoveredId !== null) {
            map.setFeatureState(
              { source: "lsgs", id: hoveredId },
              { hover: false },
            );
          }

          const feature = e.features[0];
          hoveredId = feature.id;

          map.setFeatureState(
            { source: "lsgs", id: hoveredId },
            { hover: true },
          );
          map.getCanvas().style.cursor = "pointer";

          // Update Tooltip
          const { name, lsg_type, district } = feature.properties;
          const typeColor =
            lsg_type === "municipal corporation"
              ? "#ec4899"
              : lsg_type === "municipality"
                ? "#f59e0b"
                : "#10b981";

          tooltip.innerHTML = `
            <div class="px-3 py-2">
              <div class="flex items-center gap-2 mb-1">
                <span class="w-2 h-2 rounded-full" style="background-color: ${typeColor}"></span>
                <span class="text-[10px] font-black uppercase tracking-widest text-slate-400">${lsg_type}</span>
              </div>
              <div class="text-sm font-bold text-white">${name}</div>
              <div class="text-[10px] text-slate-400 font-medium">${district} District</div>
            </div>
          `;
          tooltip.style.display = "block";
          tooltip.style.left = e.point.x + 15 + "px";
          tooltip.style.top = e.point.y + 15 + "px";
        }
      });

      map.on("mouseleave", "lsgs-fill", () => {
        if (hoveredId !== null) {
          map.setFeatureState(
            { source: "lsgs", id: hoveredId },
            { hover: false },
          );
        }
        hoveredId = null;
        map.getCanvas().style.cursor = "";
        tooltip.style.display = "none";
      });

      map.on("click", "lsgs-fill", (e) => {
        const feature = e.features[0];
        if (feature) {
          selectedLSG.set(feature.properties);

          // Center and zoom to LSG
          const lat = parseFloat(
            feature.properties.lat || feature.properties.centroid_lat,
          );
          const lon = parseFloat(
            feature.properties.lon || feature.properties.centroid_lon,
          );

          if (lat && lon) {
            map.flyTo({
              center: [lon, lat],
              zoom: 11,
              essential: true,
            });
          }
        }
      });

      mapReady.set(true);
    });

    return () => {
      if (map) map.remove();
    };
  });
</script>

<div bind:this={mapContainer} class="map-container relative">
  <div
    id="map-tooltip"
    class="fixed hidden glass rounded-xl shadow-2xl z-[100] pointer-events-none min-w-[150px] border border-white/10 overflow-hidden backdrop-blur-md"
  ></div>
</div>

<style>
  .map-container {
    width: 100%;
    height: 100%;
  }
</style>
