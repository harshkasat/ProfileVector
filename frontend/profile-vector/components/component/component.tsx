/**
 * v0 by Vercel.
 * @see https://v0.dev/t/VYFj71gQvnz
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
export default function Component() {
  return (
    <div className="flex flex-col h-screen bg-[#1e1e1e] text-[#f0f0f0] font-mono">
      <div className="flex-1 p-4 overflow-auto">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-[#9b9b9b]">user@terminal</span>
            <span className="text-[#4caf50]">~</span>
            <span className="text-[#f0f0f0]">$</span>
            <input
              type="text"
              className="bg-transparent border-none outline-none text-[#f0f0f0] w-full"
              placeholder="Enter your prompt..."
            />
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[#9b9b9b]">user@terminal</span>
              <span className="text-[#4caf50]">~</span>
              <span className="text-[#f0f0f0]">$</span>
              <span className="text-[#00bcd4]">echo "Hello, World!"</span>
            </div>
            <div className="text-[#00bcd4]">Hello, World!</div>
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[#9b9b9b]">user@terminal</span>
              <span className="text-[#4caf50]">~</span>
              <span className="text-[#f0f0f0]">$</span>
              <span className="text-[#00bcd4]">ls -la</span>
            </div>
            <div className="text-[#f0f0f0]">
              <div>total 16</div>
              <div>drwxr-xr-x 2 user user 4096 Sep 11 2024 .</div>
              <div>drwxr-xr-x 4 user user 4096 Sep 11 2024 ..</div>
              <div>-rw-r--r-- 1 user user 100 Sep 11 2024 file1.txt</div>
              <div>-rw-r--r-- 1 user user 200 Sep 11 2024 file2.txt</div>
            </div>
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[#9b9b9b]">user@terminal</span>
              <span className="text-[#4caf50]">~</span>
              <span className="text-[#f0f0f0]">$</span>
              <span className="text-[#00bcd4]">cat file1.txt</span>
            </div>
            <div className="text-[#f0f0f0]">This is the content of file1.txt.</div>
          </div>
        </div>
      </div>
      <div className="bg-[#2d2d2d] px-4 py-2 flex items-center gap-2">
        <span className="text-[#9b9b9b]">user@terminal</span>
        <span className="text-[#4caf50]">~</span>
        <span className="text-[#f0f0f0]">$</span>
        <input
          type="text"
          className="bg-transparent border-none outline-none text-[#f0f0f0] flex-1"
          placeholder="Enter your command..."
        />
      </div>
    </div>
  )
}