<script setup>
const props = defineProps({
  videoId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<template>
  <!-- 전체 화면 덮는 배경 -->
  <div class="backdrop" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>예고편</h2>
        <button class="close-btn" @click="close">X</button>
      </div>

      <div class="modal-body">
        <iframe
          v-if="videoId"
          :src="`https://www.youtube.com/embed/${videoId}`"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
        <p v-else>예고편 영상을 찾을 수 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 16px;
  border-radius: 8px;
  width: 800px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 18px;
  cursor: pointer;
}

.modal-body iframe {
  width: 100%;
  height: 450px;
  border-radius: 8px;
}
</style>
