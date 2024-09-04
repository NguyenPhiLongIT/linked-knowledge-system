<style scoped>
    .wrapper{
        height: 100vh;
    }
</style>

<template>
  <section class="wrapper">
    <v-network-graph
    :zoom-level="5"
    :nodes="nodes"
    :edges="edges"
    :layouts="layouts"
    :configs="configs"
  />
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

// const NODE_COUNT = 1

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
            .force("edge", forceLink.distance(60).strength(0.2))
            .force("charge", d3.forceManyBody().strength(-120))
            .alphaMin(0.001)
        }
      }),
    },
    node: {
      normal: {
        color: n => (n.id === "node0" ? "#ff0000" : "#4466cc"),
        radius: 32,
      },
      label: {
        visible: true,
        fontSize: 14,
      },
    },
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

// buildNetwork(NODE_COUNT, nodes, edges)

// function buildNetwork(count: number, nodes: vNG.Nodes, edges: vNG.Edges) {
//   const idNums = [...Array(count)].map((_, i) => i)

//   // nodes
//   const newNodes = idNums.map(id => [`node${id}`, { id: `node${id}` }])
//   Object.assign(nodes, Object.fromEntries(newNodes))

//   // edges
//   const makeEdgeEntry = (id1: number, id2: number) => {
//     return [`edge${id1}-${id2}`, { source: `node${id1}`, target: `node${id2}` }]
//   }
//   const newEdges = []
//   for (let i = 1; i < count; i++) {
//     newEdges.push(makeEdgeEntry(Math.floor(i / 4), i))
//   }
//   Object.assign(edges, Object.fromEntries(newEdges))
// }
</script>