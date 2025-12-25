<template>
  <Combobox v-model="selected">
    <div class="relative w-full">
      <ComboboxInput
        class="w-full form-input placeholder:text-ink-gray-4 text-base py-1.5 pl-3 pr-8 transition-colors"
        @change="query = $event.target.value"
        autocomplete="off"
        :placeholder="placeholder"
      />
      <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
        <FeatherIcon
          name="chevron-down"
          class="h-4 w-4 text-gray-500"
          aria-hidden="true"
        />
      </ComboboxButton>
      <transition
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ComboboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
        >
          <div
            v-if="filteredOptions.length === 0 && query !== ''"
            class="relative cursor-default select-none py-2 px-4 text-gray-700"
          >
            Nothing found.
          </div>

          <ComboboxOption
            v-for="option in filteredOptions"
            as="template"
            :key="option.value"
            :value="option"
            v-slot="{ selected, active }"
          >
            <li
              class="relative cursor-default select-none py-2 pl-10 pr-4"
              :class="{
                'bg-ink-gray-1 text-ink-gray-9': active,
                'text-gray-900': !active,
              }"
            >
              <span
                class="block truncate"
                :class="{ 'font-medium': selected, 'font-normal': !selected }"
              >
                {{ option.label }}
              </span>
              <span
                v-if="selected"
                class="absolute inset-y-0 left-0 flex items-center pl-3 text-ink-primary"
              >
                <FeatherIcon name="check" class="h-4 w-4" aria-hidden="true" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </transition>
    </div>
  </Combobox>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
} from '@headlessui/vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: [String, Object],
  options: {
    type: Array,
    default: () => [],
  },
  placeholder: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const query = ref('')

// Initialize selected based on modelValue
const getOption = (val) => {
  if (!val) return null
  if (typeof val === 'object') return val
  return props.options.find((o) => o.value === val) || { label: val, value: val }
}

const selected = ref(getOption(props.modelValue))

watch(
  () => props.modelValue,
  (val) => {
    selected.value = getOption(val)
  }
)

watch(selected, (val) => {
  emit('update:modelValue', val?.value)
})

const filteredOptions = computed(() =>
  query.value === ''
    ? props.options
    : props.options.filter((option) =>
        option.label
          .toLowerCase()
          .replace(/\s+/g, '')
          .includes(query.value.toLowerCase().replace(/\s+/g, ''))
      )
)
</script>
