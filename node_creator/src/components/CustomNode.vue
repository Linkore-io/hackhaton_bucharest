<script setup>
import { Handle, Position } from '@vue-flow/core'
import { NodeToolbar } from '@vue-flow/node-toolbar'

defineProps(['data', 'label'])
</script>

<template>
    <div>
        <NodeToolbar
            style="display: flex; gap: 0.5rem; align-items: center"
            :is-visible="data.toolbarVisible"
            :position="data.toolbarPosition">
            <button>Add input</button>
            <button>Add Output</button>
        </NodeToolbar>

        <div :style="{ padding: '10px 20px' }">
            {{ label }}

        </div>
        <div v-for="[key, value] in data.inputs" :style="{position: Position.Left}">
            <li>
                <Handle type="target" :position="Position.Left" /> {{ key }} : {{ value }}
            </li>
        </div>
        <div v-for="[key, value] in data.outputs" :style="{position: Position.Right}">
            <li>
                {{ key }} : {{ value }} <Handle type="target" :position="Position.Right" /> 
            </li>
        </div>
    </div>
</template>