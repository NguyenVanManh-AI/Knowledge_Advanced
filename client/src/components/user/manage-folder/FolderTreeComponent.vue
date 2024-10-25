<template>
    <div>
        <!-- Folder Name with Collapse Trigger -->
        <li class="p-title" :data-toggle="'collapse'" :href="'#collapse-' + uniqueId" role="button"
            aria-expanded="false" :aria-controls="'collapse-' + uniqueId"
            :class="{ 'text-primary p-title-primary': folderData.children.length > 0 || folderData.file.length > 0 }">
            <i class="fa-solid fa-folder"></i> {{ folderData.folder }}
        </li>
        <!-- Collapsible Content -->
        <div :class="['collapse', 'ml-6']" :id="'collapse-' + uniqueId">
            <!-- Display files in the current folder -->
            <div v-if="folderData.file && folderData.file.length">
                <div v-for="(itemFile, index) in folderData.file" :key="index">
                    <a target="_blank" :href="config.URL + itemFile.src"><i class="fa-solid fa-file"></i> {{ itemFile.name }}</a>
                </div>
            </div>
            <!-- Render children folders recursively -->
            <div v-if="folderData.children && folderData.children.length">
                <FolderTreeComponent v-for="(child, index) in folderData.children" :key="index" :folderData="child"
                    :config="config" />
            </div>
        </div>
    </div>
</template>

<script>
import config from '@/config';
export default {
    name: 'FolderTreeComponent',
    props: {
        folderData: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            config: config,
            uniqueId: Math.random().toString(36).substring(2, 15), // Generate a unique ID for each folder
        };
    },
};
</script>

<style scoped>
/* Optional styling */
.p-title {
    cursor: default;
}

.p-title-primary:hover {
    cursor: pointer;
    text-decoration: underline;
}

.ml-6 {
    margin-left: 1.5rem;
    /* Adjust margin as needed */
}
</style>