# Python Revision Sheet — ML Engineer Prep

> Quick-recall sheet. Each entry = the "say this in an interview" version, not full explanations.
> Cross-reference: full discussion lives in chat history if you need the "why" again.

---

## 1.1 Core Fundamentals

- **PEP8**: style guide — 4-space indent, snake_case vars/functions, PascalCase classes, UPPER_CASE constants. Enforced via linters (`flake8`, `ruff`), not manually.
- **Linter vs formatter**: linter *flags* issues (style, unused vars, logic smells) without running code; formatter (`black`) *auto-rewrites* code to fix style. Runs via pre-commit hook or CI.
- **Dynamically typed**: type checked at runtime, variable can rebind to any type. Still **strongly typed** — no silent `str + int` coercion (unlike JS).
- **Type casting gotchas**:
  - `int("3.5")` → `ValueError` (can't parse decimal directly)
  - `bool("False")` → `True` (non-empty string always truthy)
  - `bool` is subclass of `int` → `True == 1`
- **Floating point imprecision**: `0.1 + 0.2 != 0.3`. Binary (base-2) can't represent most decimal fractions exactly — rounding error exists *before* arithmetic happens. Fix: `math.isclose()` / `np.allclose()`, never `==` on floats.
- **`input()`** always returns `str` — must cast manually.
- **f-strings**: `f"{x:.2f}"` (2 decimals), `f"{x:.0%}"` (percent), `f"{x:,}"` (commas), `f"{x=}"` (debug shorthand — prints name=value).
- **Docstrings**: real string literals (introspectable via `.__doc__`, `help()`) vs `#` comments (stripped, dev-only). Use NumPy-style docstrings for ML code (matches sklearn/pandas convention).
- **Truthy/falsy**: `[]`, `{}`, `0`, `None`, `""` → False. `"0"` (non-empty string) → True.
- **Ternary**: `x if cond else y`. **Chained comparison**: `0.4 < p < 0.7` works in Python.
- **`for...else`**: `else` runs only if loop completes *without* `break`.
- **Loop variable reassignment** inside body doesn't affect iteration — `range()` already generated its sequence.
- **Mutable default argument trap**: `def f(x=[])` — default created ONCE at definition time, shared/mutated across calls. Fix: `x=None`, init inside.
- **No function overloading** in Python — last definition wins. Use default args, `*args`, or `functools.singledispatch`.
- **"Multiple return values"** — actually one tuple, unpacked by caller.
- **Lambda**: single-expression only, no statements/loops/assignments. Used inline (`key=lambda x: ...`), never assigned a name (PEP8 discourages).
- **Comprehensions**: `[expr for x in iterable if cond]`. `if/else` before `for` = conditional expression (picks value); `if` after `for` = filter (drops items).
- **Generator expression** `(x for x in y)` vs list comp `[x for x in y]`: same time complexity, O(1) vs O(n) space.

---

## 1.2 Built-in Data Structures

- **List**: mutable, ordered, dynamic array (like C++ vector). `append`→O(1) amortized; `insert(0,x)`/`pop(0)`→O(n) (shifts everything).
- **Slicing**: `s[start:stop:step]`. `s[::-1]` reverses.
- **Tuple**: immutable, ordered. Hashable (if contents are) → usable as dict key/set member, unlike list.
  - `(5)` is just int `5`. `(5,)` is the actual tuple — comma matters, not parens.
- **Set**: mutable, unordered, unique, hash-table backed → O(1) avg membership check (vs O(n) for list).
  - Operators: `|` union, `&` intersection, `-` difference, `^` symmetric difference.
  - `.discard()` (no error if missing) vs `.remove()` (raises `KeyError`).
- **Dict**: mutable key-value, insertion-ordered (guaranteed Python 3.7+). Hash-table backed → O(1) avg lookup/insert/delete. Keys must be hashable (immutable types only).
  - `defaultdict(int)` — auto-inits missing keys, avoids `KeyError`.
  - `Counter(iterable)` — frequency counting in one line + `.most_common(n)`.
- **String**: immutable. Every "modification" creates a new object.
  - Looping `+=` in a string-building loop is O(n²) — use `"".join(list)` instead (O(n)).
  - `s.find()` returns index/-1; `in` for boolean membership (prefer `in` for True/False checks).
  - Format generations: `%s` (legacy) → `.format()` (pre-2016) → f-strings (modern, use this).

---

## 1.3 Pythonic Thinking

- **Iterable vs Iterator**: iterable has `__iter__` (loopable); iterator has `__next__` + remembers state, raises `StopIteration` when exhausted. `for` loop = sugar for `iter()` + repeated `next()`.
- **Generators** (`yield`): lazy, one value at a time, function state frozen/resumed between calls. O(1) memory regardless of dataset size — critical for streaming/batching large data (same principle behind PyTorch `DataLoader`).
  - Can only be iterated **once** — can't reset without recreating.
- **`zip`**: pairs iterables, **stops at shortest** (use `itertools.zip_longest` to pad instead).
- **`enumerate`**: index+value together — Pythonic replacement for `range(len(x))`. Supports `start=`.
- **`map`/`filter`**: return **lazy iterators** in Python 3 (need `list()` to materialize) — comprehensions usually preferred for readability.
- **`reduce`** (from `functools`): cumulative collapse to single value. Rare in real ML code (prefer `sum()`/NumPy/Pandas reductions); conceptual ancestor of MapReduce.
- **Shallow vs deep copy**:
  - Shallow (`copy.copy()`, `.copy()`, `[:]`) — new outer container, but nested mutable elements still **shared by reference**. Mutating nested item affects original too.
  - Deep (`copy.deepcopy()`) — recursively independent copy, no shared references.
  - Danger only appears with **nested mutable structures** (list of lists/dicts).
- **Pass by object reference** (not "by value" or "by reference"): function gets reference to same object. Mutating in-place (`.append()`) affects caller; rebinding (`x = x + 1`) does not. Depends on object **mutability**, not Python's calling convention.
- **`*args`** → tuple of extra positional args. **`**kwargs`** → dict of extra keyword args.
  - Unpacking: `f(*list_vals)`, `f(**dict_config)`.
  - Valid order: `def f(a, b, *args, c=10, **kwargs)`.

---

## 1.4 OOP

- **`__init__`**: runs on instantiation; technically initializes (not creates — `__new__` creates).
- **Instance vs class variable**: instance var (`self.x`) unique per object; class var (shared across all instances) — same mutable-default-trap risk as function defaults if it's a list/dict.
- **Dunder methods**: `__repr__` (unambiguous, dev-facing, ideally recreates object), `__str__` (human-readable display), `__eq__` (controls `==`), `__len__`, `__getitem__`. `print()`/`str()` fall back to `__repr__` if `__str__` missing.
- **Inheritance**: `super().__init__()` calls parent's method — forgetting it means parent attributes never get set.
- **MRO** (Method Resolution Order): left-to-right priority in multiple inheritance (`class C(A, B)` → A wins ties). Inspect via `C.__mro__`. This is how sklearn's `BaseEstimator, TransformerMixin` combo works.
- **Polymorphism**: same method call (`.predict()`), different behavior per concrete type — the core of sklearn's consistent `.fit()/.predict()/.transform()` API.
- **Encapsulation**: `_x` = "protected" by convention only (not enforced). `__x` = name-mangled (`_ClassName__x`), harder but not impossible to access. **Python has no true private vars** — "we're all consenting adults" philosophy.
- **`@property`**: getter/setter with validation, while keeping plain-attribute-access syntax.
- **Abstraction**: `from abc import ABC, abstractmethod` — `ABC` subclass with `@abstractmethod` can't be instantiated until subclass implements the method. Mirrors sklearn's base-class contracts.
- **`@dataclass`**: auto-generates `__init__`, `__repr__`, `__eq__` from type-annotated fields. Use for data-holding classes (configs, feature records); regular class when there's real custom behavior.

---

## 1.5 Error Handling & Debugging

- **Execution order**: `try` → (if exception) `except` → `else` (**only if no exception occurred**) → `finally` (**always** runs, even with a `return` in try/except).
- **Bare `except:`** — anti-pattern, catches everything including `KeyboardInterrupt`/`SystemExit`. Always catch specific types, or `Exception` (not bare) if catching broadly.
- **Custom exceptions**: inherit from `Exception`, let calling code catch precisely what's expected while unexpected errors still propagate loudly.
- **`TypeError` vs `ValueError`**: TypeError = wrong type for the operation (`"a"+5`); ValueError = right type, invalid value (`int("3.5")`).
- Common errors to know cold: `KeyError`, `IndexError`, `AttributeError`, `NameError`, `ZeroDivisionError`, `FileNotFoundError`, `ImportError`/`ModuleNotFoundError`, `RecursionError`.
- **`raise`** alone in an `except` block re-raises the same exception (preserves traceback). **`raise X from Y`** chains exceptions, preserving original cause.

---

## 1.6 Modules, Packages & Environments

- **Import mechanics**: module executes top-to-bottom **once**, cached in `sys.modules` — re-importing elsewhere just hands back the cached object (import side-effects only happen once).
- **`from x import *`** — discouraged, pollutes namespace, hides where names came from.
- **Package** = directory + `__init__.py`. Relative imports (`from .module import x`) only work when run as part of a package, not as a standalone script — common real "why is my import broken" cause.
- **`venv`** — Python-only, pip-based, isolated environment, assumes correct interpreter already installed.
- **`conda`** — manages interpreter version *and* non-Python deps (CUDA, MKL, compiled libs) — why it dominates ML/DS specifically.
- **`requirements.txt`** (from `pip freeze`) — flat list, includes transitive deps, not always perfectly reproducible.
- **Poetry** — `pyproject.toml` (direct deps) + `poetry.lock` (exact pinned resolution incl. transitive) → guaranteed reproducible installs.
- **`if __name__ == "__main__":`** — `__name__` is `"__main__"` only when file is run directly, not when imported. Lets a file be both reusable module and runnable script without auto-executing demo code on import.

---

## 1.7 File Handling & Serialization

- **`with open(...) as f:`** — context manager, guarantees file closes even on exception (vs manual `open()`/`.close()` risking a leak if exception occurs first).
- Modes: `"r"`, `"w"` (truncates), `"a"` (append), `"x"` (create, fail if exists), `"b"` suffix = binary.
- **`load`/`dump`** = file objects. **`loads`/`dumps`** = in-memory strings. (Pattern consistent across `json` and `pickle`.)
- **JSON**: no native tuple/set — tuples serialize as arrays, deserialize back as **lists** (not type-preserving round-trip).
- **Pickle**: serializes *any* Python object (models, custom classes) — but **not human-readable, not cross-language, security risk on untrusted input** (arbitrary code execution via `__reduce__`), and version-fragile across library versions.
  - `joblib` preferred over raw pickle for sklearn models (more efficient with large NumPy arrays).
- **`pathlib`** (modern) vs **`os.path`** (legacy, string-based): `Path("a") / "b"`, `.exists()`, `.glob()`, `.stem`, `.suffix` — cross-platform safe (fixes the `\\` vs `/` Windows/Linux bug).
- **Logging > print()**: log levels (`DEBUG < INFO < WARNING < ERROR < CRITICAL`) let you control verbosity without deleting code.

---

## 1.8 NumPy

- **Why faster than lists**: contiguous memory, single fixed dtype, vectorized C-level ops — avoids per-element Python object overhead + interpreter loop.
- Every element same dtype (unlike Python lists, which mix types freely) — this homogeneity is *why* vectorization works.
- **Broadcasting rule**: compare shapes from rightmost dim backward; compatible if equal OR one is 1. Lets `(2,3) + (3,)` work without explicit loops.
- **`axis` parameter**: `axis=N` collapses/eliminates dimension N. `axis=0` sums down columns, `axis=1` sums across rows.
- **"Never loop over a NumPy array"** — vectorized ops are routinely 50-100x faster.
- **`@` (matrix mult) vs `*` (element-wise/Hadamard product)** — critical distinction; confusing them gives silently wrong results, especially relevant since `output = X @ W + b` is the literal neural net forward pass.
- **Random sampling**: `np.random.default_rng(seed=42)` (modern) — seeding makes randomness reproducible (same mechanism behind sklearn's `random_state`).

---

## 1.9 Pandas

- **Mental model**: DataFrame = dict of Series (each column), Series = NumPy array + labeled index. One dtype **per column** (vs NumPy's one dtype for whole array) — natural fit for mixed-type tabular data.
- **`.loc` (label-based) vs `.iloc` (integer position-based)** — THE most-tested Pandas distinction. Can diverge completely on a filtered/re-indexed DataFrame.
- **Must use `&`/`|`** (not `and`/`or`) for combining boolean filters — `and/or` raise `ValueError: truth value of a Series is ambiguous` since they expect a single bool, not element-wise.
- **GroupBy = split-apply-combine** — conceptually identical to SQL `GROUP BY` + aggregates.
- **`.transform()` vs `.agg()`**: agg collapses to one row per group; transform broadcasts group result back to original row count/shape.
- **Missing values**: `.isna()`/`.isnull()` (never `== np.nan`, same IEEE754 reason as `math.isnan`). `.dropna()`, `.fillna()`.
- **Merge `how=` maps directly to SQL joins**: inner/left/right/outer.
- **Duplicate-key merge danger**: non-unique join key → cross-product row inflation. Always sanity-check `.shape` before/after merge.
- **Time-series**: `pd.to_datetime()` + `.dt` accessor = vectorized version of `datetime`/`strptime`. `.rolling(window=n).mean()` for moving averages.

---

## 1.10 Data Visualization

- **Matplotlib**: low-level engine. Prefer **object-oriented interface** (`fig, ax = plt.subplots()`) over stateful `plt.plot()` for anything beyond one quick throwaway chart.
- **Seaborn**: built on Matplotlib, DataFrame-native (`data=df, x="col"`), better statistical defaults (KDE, box stats, correlation computed for you).
- **Plot selection logic** (the actual interview-tested reasoning):
  - Histogram/KDE → distribution shape of one numeric var (informs log-transform decisions)
  - Boxplot → outliers (IQR-based whiskers) + compare spread/median across categories
  - Scatterplot → relationship between two numeric vars, catches non-linear patterns correlation coefficient alone would miss
  - Correlation heatmap (`df.corr()`) → flags multicollinearity early (matters more for linear models than tree-based models like XGBoost)
  - Pairplot → pairwise relationships across many variables at once
- **EDA order of reasoning** (what to say in interviews): distribution checks → outlier/category comparison → correlation → targeted relationship plots.

---

## 1.12 Async & Parallel Python

- **GIL** (Global Interpreter Lock): only one thread executes Python bytecode at a time — root cause for why Python has 3 different concurrency tools.
- **Threading**: same process/memory. GIL means **no speedup for CPU-bound work**; helps **I/O-bound work** (GIL released while waiting on network/disk).
- **Multiprocessing**: separate processes, separate memory, own GIL each → true parallelism for **CPU-bound** work. Cost: data must be pickled/copied between processes (why unpicklable objects fail in `Pool`). This is what `n_jobs=-1` in `RandomizedSearchCV` uses internally.
- **Decision rule**: CPU-bound → multiprocessing. I/O-bound, many concurrent ops → asyncio. I/O-bound, a few ops, non-async libraries → threading.
- **`async`/`await`**: single-threaded cooperative concurrency via event loop. `async def` returns a coroutine object (not run immediately — same intuition as generators). `await` pauses at I/O wait, lets other coroutines run, resumes on completion.
- **Critical mistake**: calling a *blocking* function inside `async def` (e.g. `time.sleep()` instead of `await asyncio.sleep()`) freezes the **entire event loop** — defeats the whole point.
- Needs async-native libraries throughout (`aiohttp`, not `requests`) — one blocking call poisons the benefit.

---

## 1.14 Production-Ready Python Mindset

- **Clean code**: names that carry meaning > terse code. Functions do one thing (no "and" in the name). Flatten nesting with early returns. Name magic numbers as constants.
- **Modular design**: each module = single clear responsibility, communicates through clean interfaces. Litmus test: can you describe a module's job in one sentence without "and"?
- **Logging mindset** (beyond API mechanics): log enough to debug after the fact without drowning signal in noise; log meaningful checkpoints (start/end/counts/anomalies), not every row. Monitoring = tracking system health over time (latency, error rate, data drift).
- **Reading unfamiliar code**: find entry point → trace data flow (not every line) → read docstrings/comments first → use IDE "find usages"/grep → run it with a debugger/print statements rather than only reading statically.
- This whole section is evaluated **implicitly** throughout live coding — naming, structure, unprompted edge-case handling, not asked as a standalone question.

---

## Topics Explicitly Marked "Already Known" (Skipped)
- FastAPI
- Pydantic

## Topics Not Yet Covered
- 1.13 (covered above as skipped)
- SQL (full section)
- Software Essentials
- Cloud Fundamentals
- AI Coding

---
*Generated as part of the ML Engineer Fundamentals prep series. Update this sheet after each new section closes.*
