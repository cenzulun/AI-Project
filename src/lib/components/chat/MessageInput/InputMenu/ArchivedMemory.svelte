<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { getArchivedMemories } from '$lib/apis/chats';
	import { config } from '$lib/stores';
	import { fuzzysearch } from '$lib/utils';
	import Search from '$lib/components/common/Search.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';

	const i18n = getContext('i118n');

	export let onSelect;

	let memories = null;
	let searchVal = '';

	const init = async () => {
		memories = await getArchivedMemories(localStorage.token);
	};

	onMount(() => {
		init();
	});

	$: filteredMemories = memories
		? memories.filter((memory) => fuzzysearch(searchVal.toLowerCase(), memory.name.toLowerCase()))
		: [];
</script>

<div class="w-full text-sm">
	<Search bind:value={searchVal} placeholder={'Search Memories'} />
</div>

<div class="max-h-44 overflow-y-auto overflow-x-hidden scrollbar-thin">
	{#if memories === null}
		<div class="flex justify-center items-center h-20">
			<Spinner />
		</div>
	{:else if filteredMemories.length > 0}
		{#each filteredMemories as memory (memory.id)}
			<button
				class="flex w-full items-center text-left gap-2 px-3 py-1.5 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-xl"
				on:click={() => {
					onSelect({
						id: `collection-id:${memory.id}`,
						name: `@${memory.name}`,
						type: 'collection'
					});
				}}
			>
				{memory.name}
			</button>
		{/each}
	{:else}
		<div class="flex justify-center items-center h-20 text-xs">{$i18n.t('No memories found')}</div>
	{/if}
</div>
