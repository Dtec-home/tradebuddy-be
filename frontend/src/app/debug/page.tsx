'use client'

export default function DebugPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-4xl font-bold text-purple-600 mb-8">Debug Page</h1>
      
      <div className="space-y-6">
        {/* Basic styling test */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-md">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Basic Styling Test</h2>
          <p className="text-gray-600 mb-4">This should have a white background with gray border and shadow.</p>
          <button className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors">
            Purple Button
          </button>
        </div>

        {/* Colors test */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-red-500 text-white p-4 rounded">Red</div>
          <div className="bg-green-500 text-white p-4 rounded">Green</div>
          <div className="bg-blue-500 text-white p-4 rounded">Blue</div>
          <div className="bg-purple-500 text-white p-4 rounded">Purple</div>
          <div className="bg-yellow-500 text-white p-4 rounded">Yellow</div>
          <div className="bg-gray-500 text-white p-4 rounded">Gray</div>
        </div>

        {/* Flexbox test */}
        <div className="flex space-x-4 bg-blue-50 p-4 rounded">
          <div className="flex-1 bg-blue-200 p-4 rounded">Flex 1</div>
          <div className="flex-1 bg-blue-300 p-4 rounded">Flex 2</div>
          <div className="flex-1 bg-blue-400 p-4 rounded text-white">Flex 3</div>
        </div>

        {/* Typography test */}
        <div className="bg-white p-6 rounded border">
          <h1 className="text-6xl font-bold mb-2">Heading 1</h1>
          <h2 className="text-4xl font-semibold mb-2">Heading 2</h2>
          <h3 className="text-2xl font-medium mb-2">Heading 3</h3>
          <p className="text-lg text-gray-700 mb-2">Large paragraph text</p>
          <p className="text-base text-gray-600 mb-2">Regular paragraph text</p>
          <p className="text-sm text-gray-500">Small text</p>
        </div>
      </div>
    </div>
  )
}