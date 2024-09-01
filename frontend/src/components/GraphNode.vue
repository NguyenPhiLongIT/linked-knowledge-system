<style scoped>
    .wrapper{
        height: 100vh;
    }
</style>

<template>
  <section class="wrapper">
    <v-network-graph
    :zoom-level="1"
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

const NODE_COUNT = 1

const nodes = {
  node0: { name: "Node 0"},
  node1: { name: "Node 1" },
  node2: { name: "Node 2" },
  node3: { name: "Node 3" },
  node4: { name: "Node 4" },
  node5: { name: "Node 5" },
  node6: { name: "Node 6" },
  node7: { name: "Node 7" },
}

const edges = {
  edge1: { source: "node0", target: "node1" },
  edge2: { source: "node0", target: "node2" },
  edge3: { source: "node0", target: "node3" },
  edge4: { source: "node0", target: "node4" },
  edge5: { source: "node1", target: "node5" },
  edge6: { source: "node1", target: "node6" },
  edge7: { source: "node4", target: "node7" },
}
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
        radius: 28,
      },
      label: {
        visible: true,
        fontSize: 15,
      },
    },
  })
)

buildNetwork(NODE_COUNT, nodes, edges)

function buildNetwork(count: number, nodes: vNG.Nodes, edges: vNG.Edges) {
  const idNums = [...Array(count)].map((_, i) => i)

  // nodes
  const newNodes = idNums.map(id => [`node${id}`, { id: `node${id}` }])
  Object.assign(nodes, Object.fromEntries(newNodes))

  // edges
  const makeEdgeEntry = (id1: number, id2: number) => {
    return [`edge${id1}-${id2}`, { source: `node${id1}`, target: `node${id2}` }]
  }
  const newEdges = []
  for (let i = 1; i < count; i++) {
    newEdges.push(makeEdgeEntry(Math.floor(i / 4), i))
  }
  Object.assign(edges, Object.fromEntries(newEdges))
}
</script>