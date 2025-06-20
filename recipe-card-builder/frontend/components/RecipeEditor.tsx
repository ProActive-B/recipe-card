import { useEffect, useState } from 'react';

interface Props {
  recipeId: string;
}

interface Recipe {
  title: string;
  ingredients: string;
  steps: string;
  servings?: string;
  cook_time?: string;
}

export default function RecipeEditor({ recipeId }: Props) {
  const [recipe, setRecipe] = useState<Recipe | null>(null);

  useEffect(() => {
    fetch(`/api/recipe/${recipeId}`)
      .then((res) => res.json())
      .then((data) => setRecipe(data));
  }, [recipeId]);

  if (!recipe) return null;

  return (
    <div className="mt-4 space-y-2">
      <input
        className="border p-2 w-full"
        value={recipe.title}
        onChange={(e) => setRecipe({ ...recipe, title: e.target.value })}
      />
      <textarea
        className="border p-2 w-full"
        value={recipe.ingredients}
        onChange={(e) => setRecipe({ ...recipe, ingredients: e.target.value })}
      />
      <textarea
        className="border p-2 w-full"
        value={recipe.steps}
        onChange={(e) => setRecipe({ ...recipe, steps: e.target.value })}
      />
    </div>
  );
}
