<script setup lang="ts">

import { ref } from 'vue';
import { reactive } from 'vue';
import { markRaw } from 'vue'
import type { Elements } from '@vue-flow/core'
import { VueFlow, Node, useVueFlow, Position } from '@vue-flow/core'
import { Background, BackgroundVariant } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import CustomNode from './CustomNode.vue'

import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "@vue-flow/minimap/dist/style.css";

const { nodes, addNodes, edges, addEdges, onConnect, onPaneReady, onNodeDragStop, dimensions, findNode, setNodes, updateNodeInternals } = useVueFlow()


const defaultLabel = '-'

const opts = reactive({
  label: defaultLabel,
  inputName: "",
  inputType: "",
  outputName: "",
  outputType: ""
})
const updateNode = () => {
  const node = findNode(currentNode.NodeId)
  node.label = opts.label.trim() !== '' ? opts.label : defaultLabel
  updateNodeInternals([node.id])
}

const updateNodeAddInput = () => {
  const node = findNode(currentNode.NodeId)
  node.data.inputs.set(opts.inputName,opts.inputType);
  updateNodeInternals([node.id])
  
}

const updateNodeAddOutput = () => {
  const node = findNode(currentNode.NodeId)
  node.data.outputs = new Map<string, string>();
  node.data.outputs.set(opts.outputName,opts.outputType);
  updateNodeInternals([node.id])
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
    template: markRaw(CustomNode),
    data: {toolbarPosition: Position.Bottom, inputs: new Map<string, string>()},
    position: { x: Math.random() * dimensions.value.width, y: Math.random() * dimensions.value.height },
    selectable: true,
    events: {
      click: () => {
        currentNode.NodeId = newNode.id;
        console.log('currentNode', currentNode.NodeId);
        //newNode.data.toolbarVisible = true;
        opts.label = findNode(currentNode.NodeId).label;
      },

    },
  };
  addNodes([newNode])
}

onConnect((params) => addEdges([params]))
onPaneReady((flowInstance) => console.log('flow loaded:', flowInstance))
onNodeDragStop((node) => {
  currentNode.NodeId = node.node.id;
  opts.label = node.node.label;
})


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
      <label>Name:</label>
      <input v-model="opts.inputName" @input="updateNode" id="inputName"/>
      <label>Type:</label>
      <input v-model="opts.inputType" @input="updateNode" id="inputType"/>
      <button type="button" @click="updateNodeAddInput">Add Input</button>
      </div>
      <div id="dynamic_outputs">
        <label>Name:</label>
        <input v-model="opts.outputName" @input="updateNode" id="inputName"/>
        <label>Type:</label>
        <input v-model="opts.outputType" @input="updateNode" id="inputType"/>
        <button type="button" @click="updateNodeAddOutput">Add Output</button>
      </div>
    </div>
  </VueFlow>
</template>

<style>
.updatenode__controls{position:absolute;right:10px;top:10px;z-index:4;font-size:11px;background-color:#d3d3d3;border-radius:10px;padding:8px}
.updatenode__controls label{display:blocK}
.updatenode__controls input{padding:2px;border-radius:5px}

.vue-flow__node-custom {
  background: #9CA8B3;
  color: #fff;
  padding: 10px;
}
</style>