<script setup lang="ts">

import { ref } from 'vue';
import { reactive } from 'vue';
import type { Elements } from '@vue-flow/core'
import { VueFlow, Node, useVueFlow } from '@vue-flow/core'
import { Background, BackgroundVariant } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "@vue-flow/minimap/dist/style.css";

const { nodes, addNodes, edges, addEdges, onConnect, onPaneReady, onNodeDragStop, dimensions, findNode, setNodes, updateNodeInternals } = useVueFlow()

onConnect((params) => addEdges([params]))
onPaneReady((flowInstance) => console.log('flow loaded:', flowInstance))
onNodeDragStop((node) => console.log('drag stop', node))


const defaultLabel = '-'

const opts = reactive({
  label: defaultLabel,
})
const updateNode = () => {
  const node = findNode(currentNode.NodeId)
  node.label = opts.label.trim() !== '' ? opts.label : defaultLabel
  updateNodeInternals([node.id])
}

const updateNodeAddInput = () => {
   var container = document.getElementById("dynamic_inputs");
   var input = document.createElement("input");
   input.type = "text";
   container.appendChild(input);
}

const updateNodeAddOutput = () => {

}

interface CurrentNode {
  get NodeId(): string;
  set NodeId(value: string);
}
let currentNode: CurrentNode = {
  get NodeId() {
    return this._NodeId;
  },
  set NodeId(value: string) {
    this._NodeId = value;
  }
}

const addRandomNode = () => {
  const nodeId = (nodes.value.length + 1).toString();
  const newNode: Node = {
    id: nodeId,
    label: `Node: ${nodeId}`,
    type: 'custom',
    position: { x: Math.random() * dimensions.value.width, y: Math.random() * dimensions.value.height },
    selectable: true,
    events: {
      click: () => {
        currentNode.NodeId = newNode.id;
        console.log('currentNode', currentNode.NodeId);
        opts.label = findNode(currentNode.NodeId).label;
      },

    },
  };
  addNodes([newNode])
}
</script>
<template>
  <VueFlow>
    <MiniMap />
    <Controls />
    <Background :variant="BackgroundVariant.Lines" />

    <button type="button" :style="{ position: 'absolute', left: '10px', top: '10px', zIndex: 4 }" @click="addRandomNode">
      add node
    </button>
    <div class="updatenode__controls" id="dynamic_controls">
      <label>label:</label>
      <input v-model="opts.label" @input="updateNode"/>
      <div id="dynamic_inputs">
        <button type="button" @click="updateNodeAddInput">Add Input</button>
      </div>
      <div id="dynamic_outputs">
        <button type="button" @click="updateNodeAddOutput">Add Output</button>
      </div>
    </div>
  </VueFlow>
</template>

<style>
.updatenode__controls{position:absolute;right:10px;top:10px;z-index:4;font-size:11px;background-color:#d3d3d3;border-radius:10px;padding:8px}
.updatenode__controls label{display:blocK}
.updatenode__controls input{padding:2px;border-radius:5px}
</style>