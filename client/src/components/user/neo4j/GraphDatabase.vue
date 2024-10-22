<template>
  <div class="neo4j-browser">
    <iframe :src="neo4jBrowserUrl" frameborder="0" width="100%" height="800px"></iframe>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Thay đổi URL này thành URL của Neo4j Browser của bạn
      neo4jBrowserUrl: "https://workspace-preview.neo4j.io/workspace/query?ntid=google-oauth2%7C116361259175955640215",
    };
  },
};


// uri = "neo4j+s://ffdfad2c.databases.neo4j.io"                   # Địa chỉ database
// username = "neo4j"                                              # Username
// password = "niQisz0U5weBUMit5DuSDTxMXmDsU91qykqIEOJTA4o"        # Password
 
// MATCH (n)-[r]-(related)
// WHERE n.id CONTAINS "tuyến_thượng_thận"
// RETURN n, r, related

</script>

<style scoped>
.neo4j-browser {
  overflow: hidden;
}

iframe {
  border: none;
}
</style>