<style scoped>
    .wrapper{
        height: 100vh;
    }
</style>

<template>
  <section class="wrapper">

    <v-network-graph :zoom-level="1.75" :nodes="nodes" :edges="edges" :layouts="layouts" :configs="configs">
    <template
      #override-node-label="{
        nodeId, scale, text, x, y, config, textAnchor, dominantBaseline
      }"
    >
      <text
        x="0"
        y="-10"
        :font-size="14 * scale"
        text-anchor="middle"
        dominant-baseline="central"
        fill="#ffffff"
      >
      <tspan v-for="(line, index) in text.split(' ')" :key="index" :x="0" :dy="index === 0 ? '0em' : '1em'">
        {{ line }}
      </tspan>
      </text>
    </template>
  </v-network-graph>

  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue"
import * as vNG from "v-network-graph"
import {
  ForceLayout,
  ForceNodeDatum,
  ForceEdgeDatum,
} from "v-network-graph/lib/force-layout"
import axios from "axios"

const nodes = ref({})
const edges = ref({})
// The fixed position of the node can be specified.
const layouts = ref({
  nodes: {
    node0: {
      x: 0,
      y: 0,
      fixed: true, // Unaffected by force
    },
  },
})

const configs = reactive(
  vNG.defineConfigs({
    view: {
      layoutHandler: new ForceLayout({
        positionFixedByDrag: false,
        positionFixedByClickWithAltKey: true,
        createSimulation: (d3, nodes, edges) => {
          // d3-force parameters
          const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
          return d3
            .forceSimulation(nodes)
            .force("edge", forceLink.distance(50).strength(0.45))
            .force("charge", d3.forceManyBody().strength(-150))
            .alphaMin(0.001)
        }
      }),
    },
    node: {
      normal: {
        color: n => (n.id === 0 ? "#ff0000" : "#4466cc"),
        radius: 38,
      },
      label: {
        visible: true,
        fontSize: 14,
      },
    },
    edge: {
      marker: {
        source: {
          type: "none",
          width: 4,
          height: 4,
          margin: -1,
          offset: 0,
          units: "strokeWidth",
          color: null,
        },
        target: {
          type: "arrow",
          width: 4,
          height: 4,
          margin: -1,
          offset: 0,
          units: "strokeWidth",
          color: null,
        },
      },
    }
  })
)

getNetwork()

function getNetwork() {
  const path = 'http://localhost:5001/graph';
  axios.get(path)
    .then((res) => {
      const knowledgeNodes = res.data.nodes;
      const realationEdges = res.data.edges;

      const newNodes = {}
      knowledgeNodes.forEach((node) => {
        newNodes[`node${node.id}`] = { id:node.id,name: node.name }
      })
      nodes.value = newNodes
      const newEdges = {}
      realationEdges.forEach((edge, index) => {
        newEdges[`edge${index}`] = { source: edge.source, target: edge.target }
      })
      edges.value = newEdges
    })
    
    .catch((err) => {
      console.error(err);
    });
}
</script>